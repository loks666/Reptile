import os
import shutil
import sys

from database.mysql_init import MySQLHandler


def main():
    mysql_handler = MySQLHandler(host='localhost', user='root', password='Lx284190056', database='local')
    result = mysql_handler.query_data(
        "SELECT file_path FROM `local`.`file` WHERE `c_name` IS NULL AND `c_group` IS NULL AND `content` LIKE 's = {%';")
    # 遍历查询结果
    for entry in result:
        file_path = entry[0]

        # 构建新的文件路径，将文件后缀名从.xmp改为.lrtemplate
        new_file_path = os.path.splitext(file_path)[0] + '.lrtemplate'

        # 构建目标文件夹路径
        target_folder = r'D:\Users\Documents\预设\回收站老预设\格式错误预设'

        # 构建新文件的完整路径
        new_file_path_in_target = os.path.join(target_folder, os.path.basename(new_file_path))

        try:
            # 移动文件
            print(new_file_path_in_target)
            shutil.move(file_path, new_file_path_in_target)
            # print(f'Moved: {file_path} to {new_file_path_in_target}')
        except FileNotFoundError:
            print(f'File not found: {file_path}')
        except FileExistsError:
            print(f'File already exists in the target folder: {new_file_path_in_target}')
        except Exception as e:
            print(f'Error moving file: {file_path}\nError: {e}')
    # mysql_handler.execute_sql( "DELETE FROM `local`.`file` WHERE `c_name` IS NULL AND `c_group` IS NULL  AND `content` not LIKE '<x:xmpmeta %' AND `content` not LIKE 's = {%';")
    sys.exit()


if __name__ == '__main__':
    main()
