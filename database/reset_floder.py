import os
import shutil


def main():
    print()
    source_folder = r'D:\Users\Documents\预设\格式化文件\xmp - Copy'
    destination_folder = r'D:\Users\Documents\预设\格式化文件\xmp'
    clear_folder(r'D:\Users\Documents\预设\格式化文件\duplication_name')
    clear_folder(r'D:\Users\Documents\预设\格式化文件\not_rename')
    # 删除目标文件夹（如果存在）
    if os.path.exists(destination_folder):
        shutil.rmtree(destination_folder)
        print(f"文件夹 '{destination_folder}' 删除成功")
    # 复制文件夹
    try:
        shutil.copytree(source_folder, destination_folder)
        print(f"Folder '{source_folder}' copied to '{destination_folder}' successfully.")
    except shutil.Error as e:
        print(f"Error: {e}")
    except OSError as e:
        print(f"Error: {e}")


def clear_folder(folder_path):
    print(f"清理文件夹: {folder_path}")
    # 遍历文件夹下的所有文件
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        try:
            if os.path.isfile(file_path):
                # 如果是文件，删除文件
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")


if __name__ == '__main__':
    main()
