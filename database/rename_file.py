import os
import shutil
import sys


def rename_files(folder_path):
    # 遍历文件夹及其子文件夹
    for foldername, subfolders, filenames in os.walk(folder_path):
        for filename in filenames:
            # print(filename)
            file_path = os.path.join(foldername, filename)

            # 检查文件是否为文件而不是文件夹
            if os.path.isfile(file_path):
                # 检查文件名是否以特定字符开头
                word = "~~"
                if word in filename:
                    # 构建新文件名（去除"~~-"）
                    new_filename = filename.replace(word, "")
                    # 构建新文件的完整路径
                    new_file_path = os.path.join(foldername, new_filename)

                    # 使用shutil.move来强制覆盖文件
                    # shutil.move(file_path, new_file_path, copy_function=shutil.copy)
                    print(f'Renamed: {filename} to {new_filename}')


def get_new_filename(word, filename):
    if word in filename:
        # 构建新文件名（去除"~~-"）
        new_filename = filename.replace(word, "")

    if filename.startswith(word):
        # 构建新文件名（去除特定字符）
        new_filename = filename[len(word):]


if __name__ == "__main__":
    # folder_path = r'D:\Users\Documents\预设\回收站老预设'
    folder_path = r'D:\Users\Documents\预设\格式化文件'

    rename_files(folder_path)
    sys.exit()
