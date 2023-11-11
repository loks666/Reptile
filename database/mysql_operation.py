import hashlib
import os
import re
import shutil
import sys
from pathlib import Path

from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, MofNCompleteColumn, TaskProgressColumn, TimeElapsedColumn
from rich.progress import Progress
from rich.table import Table

from database.mysql_init import MySQLHandler

# 替换为你的文件夹路径、数据库名称和表名称
folder_path = r'D:\Users\Documents\预设\格式化文件'
database_name = 'local'

mysql_handler = MySQLHandler(host='localhost', user='root', password='Lx284190056', database=database_name)

moves = []


def get_xml_info(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            # 使用正则表达式提取 <crs:Name> 和 <crs:Group> 中的内容
            name_match = re.search(r'<crs:Name>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.*?)</rdf:li>', content,
                                   re.DOTALL)
            group_match = re.search(r'<crs:Group>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.*?)</rdf:li>', content,
                                    re.DOTALL)
            # 设置默认值
            c_name = None
            c_group = None

            if name_match is not None:
                c_name = name_match.group(1).strip()

            if group_match is not None:
                c_group = group_match.group(1).strip()

            return c_name, c_group, content
    except UnicodeDecodeError as e:
        e_str = str(e)
        # if "invalid start byte" in e_str:
        print(f"\nUnicodeDecodeError: {e_str}")
        no_match_folder = r'D:\Users\Documents\预设\removed'
        shutil.move(file_path, os.path.join(no_match_folder, os.path.basename(file_path)))
        return None, None, "exception"
    except Exception as e:
        print(f"\n其他错误: {file_path}")
        print(f"其他异常: {e}")
        return None, None, None


def save_files_to_mysql(path):
    # 实例化 MySQLHandler 类
    mysql = MySQLHandler(host='localhost', user='root', password='Lx284190056', database='local')  # 根据实际配置修改

    records = []

    path = Path(r"D:\Users\Documents\预设\格式化文件")
    # 获取文件夹下的所有文件
    file_list = list(path.glob("**/*"))
    total = len(file_list)

    job_progress = Progress(
        "{task.description}",
        BarColumn(),
        MofNCompleteColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        auto_refresh=False,
    )

    overall_progress = Progress(
        "{task.description}",
        BarColumn(),
        MofNCompleteColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn(),
        auto_refresh=False,
    )
    overall_task = overall_progress.add_task("总进度", total=total)

    progress_table = Table.grid()
    progress_table.add_row(Panel.fit(overall_progress, title="总进度", border_style="green"))
    progress_table.add_row(Panel.fit(job_progress, title="[b]子进度", border_style="red"))

    def get_direct_sub_folders(father_path):
        sub_folders = [f for f in os.listdir(father_path) if os.path.isdir(os.path.join(father_path, f))]
        return sub_folders

    # 使用 Live 类开始实时渲染进度条
    with Live(progress_table, refresh_per_second=10):
        # 获取路径的子文件夹名称列表
        sub_folder_list = get_direct_sub_folders(path)
        # 创建子文件夹名称的任务列表
        for sub_folder_name in sub_folder_list:
            total = len(list(path.glob(f"{sub_folder_name}/**/*")))
            job_progress.add_task(f"{sub_folder_name}", total=total)
        for root, dirs, files in os.walk(path):

            for file in files:
                print(file)
                # 获取文件路径
                file_path = os.path.join(root, file)
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
                records.append((file, file_path, file_hash, c_name, c_group, content))
                overall_progress.advance(overall_task
)
                # 遍历任务列表中的每个任务
                for job in job_progress.tasks:
                    # 获取任务的描述（子文件夹名称）
                    sub_folder_name = job.description
                    # 如果当前文件的路径包含子文件夹名称
                    if sub_folder_name in str(file):
                        # 推进当前任务
                        job_progress.advance(job.id)
                        break

    # 将数据批量保存到 MySQL
    insert_sql = "INSERT INTO file (file_name,file_path, raw_hash, c_name, c_group, content) VALUES (%s,%s, %s, %s, %s, %s)"
    mysql.executemany(insert_sql, records)

    # 关闭连接
    mysql.close_connection()


def get_total(folder_path):
    try:
        # 使用 os.listdir 获取文件夹下所有文件和文件夹的名称
        file_list = os.listdir(folder_path)

        # 使用列表推导式过滤出文件，不包括子文件夹
        files = [file for file in file_list if os.path.isfile(os.path.join(folder_path, file))]

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


def delete_files(file_list):
    for file_path_tuple in file_list:
        for file_path in file_path_tuple:
            try:
                os.remove(file_path)
                print(f"File deleted: {file_path}")
            except OSError as e:
                print(f"Error deleting file {file_path}: {e}")


if __name__ == '__main__':
    # create_table(mysql_handler, 'file')
    save_files_to_mysql(folder_path)
    # for move in moves:
    #     source_path, destination_path = move
    # shutil.move(source_path, destination_path)
    # delete_files(result)
    # for row in result:
    #     print(row)
    # 关闭连接
    # mysql_handler.close_connection()
    # 退出程序
    sys.exit()
