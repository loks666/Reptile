import hashlib
import os
import re
import shutil
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from rich.live import Live

from database.RichUtil import RichUtil
from database.mysql_init import MySQLHandler

print()
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1)
# 替换为你的文件夹路径、数据库名称和表名称
folder_path = r'D:\Users\Documents\预设\格式化文件\飞林预设'
database_name = 'local'

mysql_handler = MySQLHandler(host='localhost', user='root', password='Lx284190056', database=database_name)

moves = []


def get_xml_info(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # 创建 BeautifulSoup 对象
            soup = BeautifulSoup(content, 'xml')  # 使用 'xml' 作为解析器

            # 使用 BeautifulSoup 查找 <crs:Name> 和 <crs:Group> 标签
            name_tag = soup.find('crs:Name')
            group_tag = soup.find('crs:Group')

            # 设置默认值
            c_name = None
            c_group = None

            # 如果标签存在，提取 <rdf:Alt> 中的 <rdf:li> 内容
            if name_tag:
                rdf_alt_name = name_tag.find('rdf:Alt')
                if rdf_alt_name and rdf_alt_name.find('rdf:li'):
                    c_name = rdf_alt_name.find('rdf:li').get_text(strip=True)

            if group_tag:
                rdf_alt_group = group_tag.find('rdf:Alt')
                if rdf_alt_group and rdf_alt_group.find('rdf:li'):
                    c_group = rdf_alt_group.find('rdf:li').get_text(strip=True)

            return c_name, c_group, content
    except UnicodeDecodeError as e:
        e_str = str(e)
        print(f"\nUnicodeDecodeError: {e_str}")
        no_match_folder = r'D:\Users\Documents\预设\removed'
        shutil.move(file_path, os.path.join(no_match_folder, os.path.basename(file_path)))
        return None, None, "exception"
    except Exception as e:
        print(f"\n其他错误: {file_path}")
        print(f"其他异常: {e}")
        return None, None, None


def save_files_to_mysql():
    # 实例化 MySQLHandler 类
    mysql = MySQLHandler(host='localhost', user='root', password='Lx284190056', database='local')  # 根据实际配置修改

    records = []
    # 使用 RichUtil 处理进度条
    with Live(rich_util.progress_table, refresh_per_second=10):
        for root, dirs, files in os.walk(path):
            for file_name in files:
                # print(file)
                # 获取文件路径
                if file_name.endswith('.xmp'):
                    file_path = os.path.join(root, file_name)
                    # 计算文件的哈希值
                    with open(file_path, 'rb') as f:
                        file_hash = hashlib.md5(f.read()).hexdigest()
    
                    # 获取 XML 文件的信息
                    c_name, c_group, content = get_xml_info(file_path)
                    if content is None:
                        print(f"这个文件有问题:{file_path}")
                    elif "exception" in content:
                        print(f"这个文件异常：{file_path}")
    
                    # 将数据保存到 records 列表
                    records.append((file_name, file_path, file_hash, c_name, c_group, content))
                    rich_util.update_progress()

    # 将数据批量保存到 MySQL
    insert_sql = "INSERT INTO file (file_name,file_path, raw_hash, c_name, c_group, content) VALUES (%s,%s, %s, %s, %s, %s)"
    print("插入数据库中……")
    mysql.executemany(insert_sql, records)

    # 关闭连接
    mysql.close_connection()
    rich_util.close_progress()


def get_total():
    try:
        # 使用 os.listdir 获取文件夹下所有文件和文件夹的名称
        files = os.listdir(folder_path)
        # 使用列表推导式过滤出文件，不包括子文件夹
        files = [file for file in files if os.path.isfile(os.path.join(folder_path, file))]
        # 获取文件数量
        file_count = len(files)
        return file_count
    except Exception as e:
        print(f"Error counting files: {e}")
        return None


def create_table(mysql, table):
    # 检查表是否存在
    check_table_sql = f"SHOW TABLES LIKE '{table}'"
    table_result = mysql.query_data(check_table_sql)

    if table_result:
        # 获取 AUTO_INCREMENT 列的名字
        auto_increment_column_name_query = mysql.query_data(
            f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{table}' AND EXTRA = 'auto_increment'")

        if auto_increment_column_name_query:
            auto_increment_column_name = auto_increment_column_name_query[0][0]
            # 将 AUTO_INCREMENT 列的值重置为1
            reset_auto_increment_sql = f"ALTER TABLE {table} AUTO_INCREMENT = 1"
            mysql.execute_sql(reset_auto_increment_sql)

        # 表存在，删除重建
        drop_table_sql = f"DROP TABLE {table}"
        mysql.execute_sql(drop_table_sql)

    # 创建表
    create_table_sql = "CREATE TABLE `file` (  `id` int NOT NULL AUTO_INCREMENT,  `file_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,  `raw_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,  `file_path` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,  `c_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,  `c_group` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,  `content` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin,  `new_hash` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,  PRIMARY KEY (`id`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;"
    mysql.execute_sql(create_table_sql)


def delete_files(files):
    for file_path_tuple in files:
        for file_path in file_path_tuple:
            try:
                os.remove(file_path)
                print(f"File deleted: {file_path}")
            except OSError as e:
                print(f"Error deleting file {file_path}: {e}")


if __name__ == '__main__':
    create_table(mysql_handler, 'file')

    path = Path(folder_path)
    # 获取文件夹下的所有文件
    file_list = list(path.glob("**/*"))
    total = len(file_list)
    rich_util = RichUtil(total)  # 设置总任务数

    save_files_to_mysql()
    sys.exit()
