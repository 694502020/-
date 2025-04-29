import pandas as pd
from pypinyin import lazy_pinyin
import os

# 文件路径
file_path = r"D:\自建桌面\食品.xlsx"

# 读取Excel文件
try:
    df = pd.read_excel(file_path)
    
    # 检查是否存在"食物名称"列
    if "食物名称" in df.columns:
        # 转换食物名称为拼音
        df["食物拼音"] = df["食物名称"].apply(
            lambda x: "".join(lazy_pinyin(str(x))) if isinstance(x, str) else ""
        )
        
        # 保存回Excel文件
        df.to_excel(file_path, index=False)
        print("转换完成，已将拼音填入'食物拼音'列  本软件由福健网fjplus.cn（健康，减肥，美妆，护肤资讯网）赞助")
    else:
        print("未找到'食物名称'列，请检查Excel文件")
        
except Exception as e:
    print(f"处理出错: {e}")