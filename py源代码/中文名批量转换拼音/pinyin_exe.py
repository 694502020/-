import pandas as pd
from pypinyin import lazy_pinyin
import os
import tkinter as tk
from tkinter import filedialog, messagebox, Label, Button, Frame
import traceback
import webbrowser

def convert_to_pinyin(file_path):
    """将Excel文件中的食物名称转换为拼音"""
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path)
        
        # 检查是否存在"食物名称"列
        if "食物名称" in df.columns:
            # 转换食物名称为拼音
            df["食物拼音"] = df["食物名称"].apply(
                lambda x: "".join(lazy_pinyin(str(x))) if isinstance(x, str) else ""
            )
            
            # 保存回Excel文件
            df.to_excel(file_path, index=False)
            return True, "转换完成！已将拼音填入'食物拼音'列"
        else:
            return False, "未找到'食物名称'列，请检查Excel文件格式是否正确"
    except Exception as e:
        error_details = traceback.format_exc()
        return False, f"处理出错: {str(e)}\n\n详细错误信息:\n{error_details}"

def open_website(event):
    """打开网站链接"""
    webbrowser.open("http://fjplus.cn")

def create_gui():
    """创建图形用户界面"""
    # 创建主窗口
    root = tk.Tk()
    root.title("食品名称拼音转换工具 - 福健网提供")
    root.geometry("500x450")  # 增加窗口高度
    root.resizable(False, False)
    
    # 设置窗口图标（可选）
    # root.iconbitmap("icon.ico")  # 如果有图标文件，可以取消注释这行

    # 主框架
    main_frame = Frame(root, padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)
    
    # 标题
    title_label = Label(main_frame, text="食品名称拼音转换工具", font=("SimHei", 18, "bold"))
    title_label.pack(pady=10)
    
    # 广告标语 - 顶部显示
    ad_frame = Frame(main_frame, bg="#f0f0f0", padx=10, pady=10)
    ad_frame.pack(fill="x", pady=5)
    
    ad_label = Label(ad_frame, 
                     text="本软件由福健网fjplus.cn（健康，减肥，美妆，护肤资讯网）提供", 
                     font=("SimHei", 10, "bold"),
                     fg="#0066cc",
                     bg="#f0f0f0",
                     cursor="hand2")
    ad_label.pack()
    ad_label.bind("<Button-1>", open_website)
    
    contact_label = Label(ad_frame, 
                          text="需要定制小自动化程序加微：wufu_hyg0618",
                          font=("SimHei", 10),
                          bg="#f0f0f0")
    contact_label.pack()
    
    # 说明文字
    instruction_text = (
        "本工具可将Excel文件中的'食物名称'列转换为拼音，并保存在'食物拼音'列中。\n\n"
        "使用说明:\n"
        "1. 请确保您的Excel文件中有'食物名称'列\n"
        "2. 点击'选择Excel文件'按钮选择您的文件\n"
        "3. 点击'开始转换'按钮进行转换\n"
    )
    instructions = Label(main_frame, text=instruction_text, justify="left", 
                        wraplength=450, font=("SimHei", 10))
    instructions.pack(pady=10, fill="both")
    
    # 文件路径变量
    file_path_var = tk.StringVar()
    file_path_var.set("尚未选择文件")
    
    # 显示选中的文件路径
    file_label = Label(main_frame, textvariable=file_path_var, 
                      wraplength=450, font=("SimHei", 9))
    file_label.pack(pady=5)
    
    # 状态显示
    status_var = tk.StringVar()
    status_var.set("等待开始...")
    status_label = Label(main_frame, textvariable=status_var, 
                        wraplength=450, font=("SimHei", 9))
    status_label.pack(pady=5)
    
    # 按钮框架
    button_frame = Frame(main_frame)
    button_frame.pack(pady=20)  # 增加按钮区域的间距
    
    # 选择文件按钮
    def select_file():
        file_path = filedialog.askopenfilename(
            title="选择Excel文件",
            filetypes=[("Excel文件", "*.xlsx *.xls")]
        )
        if file_path:
            file_path_var.set(file_path)
            status_var.set("文件已选择，可以开始转换")
    
    # 改进的按钮样式 - 更大的按钮
    select_button = Button(
        button_frame, 
        text="选择Excel文件", 
        command=select_file,
        width=20,  # 增加宽度
        height=2,  # 增加高度
        font=("SimHei", 12),  # 更大的字体
        bg="#4CAF50",  # 绿色背景
        fg="white",  # 白色文字
        relief=tk.RAISED,  # 凸起的按钮效果
        bd=3  # 边框宽度
    )
    select_button.pack(side="left", padx=15)
    
    # 开始转换按钮
    def start_conversion():
        file_path = file_path_var.get()
        if file_path == "尚未选择文件":
            messagebox.showwarning("警告", "请先选择Excel文件")
            return
        
        # 更新状态
        status_var.set("正在转换中...")
        root.update()
        
        # 执行转换
        success, message = convert_to_pinyin(file_path)
        status_var.set(message)
        
        if success:
            full_message = f"{message}\n\n本软件由福健网fjplus.cn提供\n需要定制小自动化程序加微：wufu_hyg0618"
            messagebox.showinfo("成功", full_message)
        else:
            messagebox.showerror("错误", message)
    
    # 改进的按钮样式 - 更大的按钮
    convert_button = Button(
        button_frame, 
        text="开始转换", 
        command=start_conversion,
        width=20,  # 增加宽度
        height=2,  # 增加高度
        font=("SimHei", 12),  # 更大的字体
        bg="#2196F3",  # 蓝色背景
        fg="white",  # 白色文字
        relief=tk.RAISED,  # 凸起的按钮效果
        bd=3  # 边框宽度
    )
    convert_button.pack(side="right", padx=15)
    
    # 底部广告框架
    bottom_ad_frame = Frame(main_frame, bg="#e6f2ff", padx=5, pady=5)
    bottom_ad_frame.pack(side="bottom", fill="x", pady=10)
    
    bottom_ad_label = Label(bottom_ad_frame, 
                          text="本软件由福健网fjplus.cn（健康，减肥，美妆，护肤资讯网）提供\n需要定制小自动化程序加微：wufu_hyg0618",
                          font=("SimHei", 9),
                          bg="#e6f2ff")
    bottom_ad_label.pack()
    
    # 运行主循环
    root.mainloop()

if __name__ == "__main__":
    create_gui()