import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

def transfer_files():
    # 获取用户选择的路径
    source_folder = source_entry.get()
    image_names_file = names_entry.get()
    destination_folder = dest_entry.get()
    
    # 验证路径
    if not all([source_folder, image_names_file, destination_folder]):
        messagebox.showerror("错误", "请填写所有路径信息")
        return
        
    # 确保目标文件夹存在
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        result_text.insert(tk.END, f"创建目标文件夹: {destination_folder}\n")
    
    # 读取需要迁移的图片名称
    image_names = []
    try:
        with open(image_names_file, 'r', encoding='utf-8') as file:
            image_names = [line.strip() for line in file if line.strip()]
        result_text.insert(tk.END, f"从文件中读取了 {len(image_names)} 个图片名称\n")
    except Exception as e:
        result_text.insert(tk.END, f"读取图片名称文件时出错: {e}\n")
        return
    
    # 开始迁移图片
    successful_count = 0
    failed_count = 0
    failed_images = []
    
    for image_name in image_names:
        source_path = os.path.join(source_folder, image_name)
        dest_path = os.path.join(destination_folder, image_name)
        
        try:
            if os.path.exists(source_path):
                # 使用move代替copy2实现剪切功能
                shutil.move(source_path, dest_path)
                successful_count += 1
                result_text.insert(tk.END, f"成功移动: {image_name}\n")
                # 自动滚动到最新内容
                result_text.see(tk.END)
            else:
                failed_count += 1
                failed_images.append(image_name)
                result_text.insert(tk.END, f"文件不存在: {image_name}\n")
                result_text.see(tk.END)
        except Exception as e:
            failed_count += 1
            failed_images.append(image_name)
            result_text.insert(tk.END, f"移动 {image_name} 时出错: {e}\n")
            result_text.see(tk.END)
    
    # 打印迁移结果摘要
    result_text.insert(tk.END, "\n本次服务由健康养生，美容护肤网（fjplus.cn）提供\n")
    result_text.insert(tk.END, "\n需要定制小自动化程序加微：wufu_hyg0618\n")		
    result_text.insert(tk.END, "\n迁移完成摘要:\n")
    result_text.insert(tk.END, f"总共需要迁移的图片: {len(image_names)}\n")
    result_text.insert(tk.END, f"成功迁移的图片: {successful_count}\n")
    result_text.insert(tk.END, f"失败的图片: {failed_count}\n")
    
    # 如果有失败的图片，将它们写入日志文件
    if failed_images:
        log_file = os.path.join(destination_folder, "failed_images.log")
        try:
            with open(log_file, 'w', encoding='utf-8') as file:
                for image in failed_images:
                    file.write(f"{image}\n")
            result_text.insert(tk.END, f"失败的图片名称已写入日志文件: {log_file}\n")
        except Exception as e:
            result_text.insert(tk.END, f"写入日志文件时出错: {e}\n")
    
    messagebox.showinfo("完成", f"文件移动完成！成功: {successful_count}, 失败: {failed_count}")

def browse_source():
    folder = filedialog.askdirectory(title="选择源文件夹")
    if folder:
        source_entry.delete(0, tk.END)
        source_entry.insert(0, folder)

def browse_names_file():
    file = filedialog.askopenfilename(title="选择包含图片名称的文本文件", filetypes=[("文本文件", "*.txt")])
    if file:
        names_entry.delete(0, tk.END)
        names_entry.insert(0, file)

def browse_destination():
    folder = filedialog.askdirectory(title="选择目标文件夹")
    if folder:
        dest_entry.delete(0, tk.END)
        dest_entry.insert(0, folder)

# 创建GUI界面
root = tk.Tk()
root.title("文件批量搬运工具")
root.geometry("600x500")

# 设置主框架
main_frame = tk.Frame(root, padx=10, pady=10)
main_frame.pack(fill=tk.BOTH, expand=True)

# 源文件夹选择
source_frame = tk.Frame(main_frame)
source_frame.pack(fill=tk.X, pady=5)
tk.Label(source_frame, text="源文件夹:", width=10).pack(side=tk.LEFT)
source_entry = tk.Entry(source_frame)
source_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
tk.Button(source_frame, text="浏览...", command=browse_source).pack(side=tk.LEFT)

# 图片名称文件选择
names_frame = tk.Frame(main_frame)
names_frame.pack(fill=tk.X, pady=5)
tk.Label(names_frame, text="图片名称文件:", width=10).pack(side=tk.LEFT)
names_entry = tk.Entry(names_frame)
names_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
tk.Button(names_frame, text="浏览...", command=browse_names_file).pack(side=tk.LEFT)

# 目标文件夹选择
dest_frame = tk.Frame(main_frame)
dest_frame.pack(fill=tk.X, pady=5)
tk.Label(dest_frame, text="目标文件夹:", width=10).pack(side=tk.LEFT)
dest_entry = tk.Entry(dest_frame)
dest_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
tk.Button(dest_frame, text="浏览...", command=browse_destination).pack(side=tk.LEFT)

# 开始按钮
tk.Button(main_frame, text="开始迁移文件", command=transfer_files, bg="#4CAF50", fg="white", padx=10, pady=5).pack(pady=10)

# 结果显示区域
result_frame = tk.Frame(main_frame)
result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
tk.Label(result_frame, text="操作日志:").pack(anchor=tk.W)

result_scroll = tk.Scrollbar(result_frame)
result_scroll.pack(side=tk.RIGHT, fill=tk.Y)

result_text = tk.Text(result_frame, height=15, yscrollcommand=result_scroll.set)
result_text.pack(fill=tk.BOTH, expand=True)
result_scroll.config(command=result_text.yview)

# 版权信息
tk.Label(root, text="文件批量搬运工具 v1.0", fg="gray").pack(side=tk.BOTTOM, pady=5)

root.mainloop()