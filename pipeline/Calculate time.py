import argparse
import os
import pandas as pd

# 主文件夹路径
parser = argparse.ArgumentParser(description="Summarize per-membrane processing times.")
parser.add_argument("--base-dir", required=True, help="Directory containing per-image result folders.")
base_dir = parser.parse_args().base_dir

results = []

# 遍历主文件夹下的每个样品文件夹
for folder in os.listdir(base_dir):
    sub_path = os.path.join(base_dir, folder, "时间统计.csv")
    if os.path.exists(sub_path):
        try:
            # 读取两列格式的CSV文件
            df = pd.read_csv(sub_path)
            if "项目" in df.columns and "数值" in df.columns:
                # 查找图像总处理时间(秒)对应的数值
                value = df.loc[df["项目"] == "图像总处理时间(秒)", "数值"]
                if not value.empty:
                    results.append({"样品名称": folder, "图像总处理时间(秒)": float(value.iloc[0])})
        except Exception as e:
            print(f"读取 {sub_path} 时出错: {e}")

# 汇总结果
summary_df = pd.DataFrame(results)

if not summary_df.empty:
    avg_time = summary_df["图像总处理时间(秒)"].mean()
    print("各样品图像总处理时间统计：")
    print(summary_df)
    print(f"\n平均图像总处理时间(秒)：{avg_time:.2f}")

    # 保存汇总结果
    output_path = os.path.join(base_dir, "处理时间汇总.csv")
    summary_df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\n已将结果保存至: {output_path}")
else:
    print("未找到任何有效的时间统计.csv 文件或格式不匹配。")
