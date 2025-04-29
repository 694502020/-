import os
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox
import threading

# 导入PIL库
try:
    from PIL import Image
except ImportError:
    # 这里不自动安装，因为打包后应该已包含所有依赖
    print("错误：未找到PIL库，请确保程序包含所有必要的依赖")
    sys.exit(1)

class ImageConverter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("JPG、jpeg转WebP工具")
        self.root.geometry("500x300")
        self.root.resizable(False, False)
        
        # 设置中文字体
        self.root.option_add("*Font", "微软雅黑 10")
        
        # 创建UI元素
        self.setup_ui()
        
        # 初始化状态变量
        self.is_converting = False
        
    def setup_ui(self):
        # 输入文件夹选择
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(input_frame, text="JPG图片文件夹:").pack(side=tk.LEFT)
        self.input_path = tk.StringVar()
        entry_input = tk.Entry(input_frame, textvariable=self.input_path, width=30)
        entry_input.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        tk.Button(input_frame, text="浏览...", command=self.select_input_folder).pack(side=tk.RIGHT)
        
        # 输出文件夹选择
        output_frame = tk.Frame(self.root)
        output_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(output_frame, text="WebP输出文件夹:").pack(side=tk.LEFT)
        self.output_path = tk.StringVar()
        entry_output = tk.Entry(output_frame, textvariable=self.output_path, width=30)
        entry_output.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        tk.Button(output_frame, text="浏览...", command=self.select_output_folder).pack(side=tk.RIGHT)
        
        # 转换按钮
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.convert_button = tk.Button(button_frame, text="开始转换", command=self.start_conversion, bg="#4CAF50", fg="white", height=2)
        self.convert_button.pack(fill=tk.X)
        
        # 状态信息
        status_frame = tk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.status_var = tk.StringVar()
        self.status_var.set("准备就绪，请选择文件夹")
        status_label = tk.Label(status_frame, textvariable=self.status_var, anchor=tk.W)
        status_label.pack(fill=tk.X)
        
        # 进度显示
        progress_frame = tk.Frame(self.root)
        progress_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.progress_var = tk.StringVar()
        self.progress_var.set("")
        progress_label = tk.Label(progress_frame, textvariable=self.progress_var, anchor=tk.W)
        progress_label.pack(fill=tk.X)
        
    def select_input_folder(self):
        folder = filedialog.askdirectory(title="选择包含JPG图片的文件夹")
        if folder:
            self.input_path.set(folder)
            # 默认将输出路径设为与输入路径相同
            if not self.output_path.get():
                self.output_path.set(folder)
    
    def select_output_folder(self):
        folder = filedialog.askdirectory(title="选择WebP图片的输出文件夹")
        if folder:
            self.output_path.set(folder)
    
    def start_conversion(self):
        if self.is_converting:
            return
        
        input_folder = self.input_path.get()
        output_folder = self.output_path.get()
        
        if not input_folder:
            messagebox.showerror("错误", "请选择输入文件夹")
            return
        
        if not os.path.exists(input_folder):
            messagebox.showerror("错误", f"输入文件夹不存在: {input_folder}")
            return
        
        if not output_folder:
            output_folder = input_folder
        
        # 在新线程中运行转换过程
        self.is_converting = True
        self.convert_button.config(state=tk.DISABLED)
        self.status_var.set("正在转换中...    本次服务由健康减肥、美容养颜资讯网（fjplus.cn）为您提供，要定制程序请加v")
        self.progress_var.set("")
        
        thread = threading.Thread(target=self.convert_jpg_to_webp, args=(input_folder, output_folder))
        thread.daemon = True
        thread.start()
    
    def convert_jpg_to_webp(self, input_folder, output_folder):
        try:
            # 确保输出文件夹存在
            os.makedirs(output_folder, exist_ok=True)
            
            # 计数器
            total_files = 0
            converted_files = 0
            
            # 首先计算总文件数
            jpg_files = list(Path(input_folder).glob("**/*.jpg"))
            total_files = len(jpg_files)
            
            if total_files == 0:
                self.update_status("未找到JPG文件")
                self.is_converting = False
                self.convert_button.config(state=tk.NORMAL)
                return
            
            # 遍历文件夹中的所有文件
            for i, file_path in enumerate(jpg_files):
                try:
                    # 更新进度
                    progress = f"正在处理: {i+1}/{total_files} - {file_path.name}"
                    self.update_progress(progress)
                    
                    # 打开JPG图片
                    img = Image.open(file_path)
                    
                    # 计算相对路径以在输出文件夹中保持目录结构
                    try:
                        rel_path = file_path.relative_to(input_folder)
                    except ValueError:
                        # 如果不是相对路径，就使用文件名
                        rel_path = file_path.name
                    
                    out_path = Path(output_folder) / rel_path
                    
                    # 确保输出目录存在
                    os.makedirs(out_path.parent, exist_ok=True)
                    
                    # 创建同名但扩展名为.webp的新文件路径
                    webp_path = out_path.with_suffix('.webp')
                    
                    # 转换并保存为WebP格式
                    img.save(webp_path, 'WEBP')
                    
                    converted_files += 1
                    
                except Exception as e:
                    self.update_progress(f"转换 {file_path.name} 时出错: {e}")
            
            # 转换完成
            self.update_status(f"转换完成! 总计 {total_files} 个JPG文件，成功转换 {converted_files} 个文件")
        
        except Exception as e:
            self.update_status(f"转换过程中出错: {e}")
        
        finally:
            self.is_converting = False
            self.convert_button.config(state=tk.NORMAL)
            self.progress_var.set("")
    
    def update_status(self, message):
        # 在主线程中更新UI
        self.root.after(0, lambda: self.status_var.set(message))
    
    def update_progress(self, message):
        # 在主线程中更新UI
        self.root.after(0, lambda: self.progress_var.set(message))
    
    def run(self):
        # 支持命令行方式启动并传递参数
        if len(sys.argv) > 1:
            input_folder = sys.argv[1]
            self.input_path.set(input_folder)
            
            if len(sys.argv) > 2:
                output_folder = sys.argv[2]
                self.output_path.set(output_folder)
        
        self.root.mainloop()

if __name__ == "__main__":
    converter = ImageConverter()
    converter.run()