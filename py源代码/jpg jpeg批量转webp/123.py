import os
import glob
from PIL import Image
import time

def convert_jpg_to_webp(source_folder, output_folder, quality=80):
    """
    将指定文件夹中的所有JPG/JPEG图片转换为WebP格式
    
    Args:
        source_folder: 源图片所在的文件夹路径
        output_folder: 输出WebP图片的文件夹路径
        quality: WebP图片质量（0-100），默认80
    """
    # 确保源路径以斜杠结尾
    if not source_folder.endswith('/') and not source_folder.endswith('\\'):
        source_folder += os.path.sep
    
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)
        
    # 获取所有JPG和JPEG文件路径
    jpg_files = glob.glob(f"{source_folder}*.jpg")
    jpeg_files = glob.glob(f"{source_folder}*.jpeg")
    all_files = jpg_files + jpeg_files
    
    # 计算总文件数
    total_files = len(all_files)
    print(f"找到 {total_files} 个JPG/JPEG文件等待转换...")
    
    # 如果没有找到文件
    if total_files == 0:
        print(f"在'{source_folder}'目录中没有找到JPG或JPEG文件。")
        return
    
    # 记录开始时间
    start_time = time.time()
    
    # 转换计数器
    success_count = 0
    failed_files = []
    
    # 转换所有图片
    for idx, img_path in enumerate(all_files, 1):
        try:
            # 获取文件基本名称(不含扩展名)
            file_name = os.path.basename(img_path)
            name_without_ext = os.path.splitext(file_name)[0]
            
            # 构建输出文件路径（在指定的输出文件夹中）
            output_path = os.path.join(output_folder, f"{name_without_ext}.webp")
            
            # 打开图片
            with Image.open(img_path) as img:
                # 转换为RGB模式(如果是RGBA,保留透明度)
                if img.mode in ('RGBA', 'LA'):
                    # 保留Alpha通道
                    img_converted = img
                else:
                    # 转换为RGB
                    img_converted = img.convert("RGB")
                
                # 保存为WebP格式
                img_converted.save(output_path, "WEBP", quality=quality)
                
                # 更新成功计数
                success_count += 1
                
                # 打印进度
                print(f"处理中: [{idx}/{total_files}] {file_name} -> {output_path}")
                
        except Exception as e:
            failed_files.append((img_path, str(e)))
            print(f"转换失败 {img_path}: {e}")
    
    # 计算耗时
    elapsed_time = time.time() - start_time
    
    # 打印结果
    print("\n" + "="*50)
    print(f"转换完成! 耗时: {elapsed_time:.2f} 秒")
    print(f"成功转换: {success_count}/{total_files} 文件")
    
    # 如果有失败的文件，打印详情
    if failed_files:
        print(f"\n转换失败的文件 ({len(failed_files)}):")
        for failed_file, error in failed_files:
            print(f" - {failed_file}: {error}")

if __name__ == "__main__":
    # 自定义图片文件夹路径 (修改此处以指定您的图片文件夹)
    IMAGE_FOLDER = "D:\自建桌面\新建文件夹 (2)"
    
    # 输出文件夹路径 (您指定的保存路径)
    OUTPUT_FOLDER = r"D:\自建桌面\新建文件夹 (3)\图片2"
    
    # 设置WebP质量 (0-100)
    WEBP_QUALITY = 85
    
    print(f"开始转换 '{IMAGE_FOLDER}' 目录下的JPG/JPEG文件为WebP格式...")
    print(f"转换后的WebP文件将保存到: '{OUTPUT_FOLDER}'")
    convert_jpg_to_webp(IMAGE_FOLDER, OUTPUT_FOLDER, quality=WEBP_QUALITY)