param(
    [string]$Repository = "23Chloe/Microplastics-Identification",
    [string]$Tag = "model-weights-v1",
    [string]$Target = "original-pool-batch",
    [Parameter(Mandatory = $true)]
    [string]$AssetDirectory
)

$ErrorActionPreference = "Stop"

$expected = [ordered]@{
    "detr_r50_author_candidate.pth" = "306c04aeffa786115586aebdd3f6e5fe649a70e55d70ef45b78cc3cdc18561f9"
    "faster_rcnn_resnet50_best.pth" = "786ae32dab7eff26f5c796a2712409e3f9dab8a4d2e3d731f2f2abd4c957c402"
    "yolov5m_best.pt" = "e2ad14dd362659707062fb20859506f0ea6ae4e6749f5faeedaaec82d97576f4"
    "yolov5n_best.pt" = "3e8d3cbcd061041443e32ed4a48380c254f4e7c8342b41920efd1b151aa38ea8"
    "yolov5s_best.pt" = "e57abc6aaa723c4298f4ce5d7da52bdda9724d16e2bdc79decdf474b5918a1ea"
    "yolov7_best.pt" = "f1359901761d03dea3fcd70710959988b83c912d581c53bc6cd6cbade3f9e804"
    "yolov7-e6e_best.pt" = "1339df3a0fcd5f59ba1c3040602f29313876c68c5f827c012fcc2d7b4b8c6b5d"
    "yolov7x_best.pt" = "2d31044a89d20d7f1ea654702736b7b26b2dd2783329d31152cee22c8bba59fb"
    "yolov8m_best.pt" = "a9a706be280ab1e4df7028d673dd111e3962f07cf1deba6cdbb3a6235afef46a"
    "yolov8n_best.pt" = "d9c2b2b8e3af88539136d67396fd4dd735cd624ba163f1f3d4cd0dd6b9939696"
    "yolov8s_best.pt" = "b8dfbb2cfcb9ccce13f353e0e9e60d23045e597fe0fcfcab45169089119d103d"
}

foreach ($entry in $expected.GetEnumerator()) {
    $path = Join-Path $AssetDirectory $entry.Key
    if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
        throw "Missing release asset: $path"
    }
    $actual = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($actual -ne $entry.Value) {
        throw "SHA-256 mismatch for $($entry.Key): $actual"
    }
}

$credentialInput = "protocol=https`nhost=github.com`n`n"
$credentialLines = $credentialInput | git credential fill
if ($LASTEXITCODE -ne 0) {
    throw "Git credential lookup failed."
}
$credential = @{}
foreach ($line in $credentialLines) {
    $separator = $line.IndexOf("=")
    if ($separator -gt 0) {
        $credential[$line.Substring(0, $separator)] = $line.Substring($separator + 1)
    }
}
if (-not $credential.ContainsKey("password")) {
    throw "No GitHub credential was returned by Git Credential Manager."
}

$headers = @{
    Accept = "application/vnd.github+json"
    Authorization = "Bearer $($credential.password)"
    "X-GitHub-Api-Version" = "2022-11-28"
    "User-Agent" = "Microplastics-Identification-release-publisher"
}

$apiBase = "https://api.github.com/repos/$Repository"
try {
    $release = Invoke-RestMethod -Uri "$apiBase/releases/tags/$Tag" -Headers $headers -Method Get
    Write-Output "Using existing release $($release.html_url)"
}
catch {
    if ($_.Exception.Response.StatusCode.value__ -ne 404) {
        throw
    }
    $body = @{
        tag_name = $Tag
        target_commitish = $Target
        name = "Model checkpoints v1"
        body = @"
Archived model checkpoints for the reproducibility package.

- YOLOv5, YOLOv7, YOLOv8, and Faster R-CNN files are the selected checkpoints recovered from the supplied archive.
- `detr_r50_author_candidate.pth` is structurally compatible with the three-class author configuration, but the retained archive does not prove that it was the checkpoint used for every reported DETR result.
- File sizes and SHA-256 values are documented in the model-specific `weights/README.md` files on the `original-pool-batch` branch.
- Training images and labels are not included in this release.
"@
        draft = $false
        prerelease = $false
        generate_release_notes = $false
    } | ConvertTo-Json
    $release = Invoke-RestMethod -Uri "$apiBase/releases" -Headers $headers -Method Post -Body $body -ContentType "application/json"
    Write-Output "Created release $($release.html_url)"
}

$assets = @($release.assets)
foreach ($entry in $expected.GetEnumerator()) {
    $name = $entry.Key
    $path = Join-Path $AssetDirectory $name
    $localSize = (Get-Item -LiteralPath $path).Length
    $existing = @($assets | Where-Object { $_.name -eq $name })
    if ($existing.Count -eq 1 -and $existing[0].state -eq "uploaded" -and $existing[0].size -eq $localSize) {
        Write-Output "Skipping existing asset: $name"
        continue
    }
    foreach ($stale in $existing) {
        Write-Output "Deleting incomplete asset: $name"
        Invoke-RestMethod -Uri "$apiBase/releases/assets/$($stale.id)" -Headers $headers -Method Delete
    }
    $encodedName = [Uri]::EscapeDataString($name)
    $uploadUrl = "https://uploads.github.com/repos/$Repository/releases/$($release.id)/assets?name=$encodedName"
    $uploaded = $null
    for ($attempt = 1; $attempt -le 3; $attempt++) {
        try {
            Write-Output "Uploading: $name (attempt $attempt of 3)"
            $uploaded = Invoke-RestMethod -Uri $uploadUrl -Headers $headers -Method Post -InFile $path -ContentType "application/octet-stream"
            break
        }
        catch {
            if ($attempt -eq 3) {
                throw
            }
            Write-Output "Upload interrupted; retrying: $name"
            $current = Invoke-RestMethod -Uri "$apiBase/releases/$($release.id)/assets" -Headers $headers -Method Get
            foreach ($stale in @($current | Where-Object { $_.name -eq $name })) {
                Invoke-RestMethod -Uri "$apiBase/releases/assets/$($stale.id)" -Headers $headers -Method Delete
            }
            Start-Sleep -Seconds (5 * $attempt)
        }
    }
    Write-Output "Uploaded: $($uploaded.browser_download_url)"
}

$verified = Invoke-RestMethod -Uri "$apiBase/releases/tags/$Tag" -Headers $headers -Method Get
Write-Output "Release: $($verified.html_url)"
Write-Output "Assets: $(@($verified.assets).Count)"
