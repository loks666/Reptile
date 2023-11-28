import re
import shutil
from collections import defaultdict
from pathlib import Path

from database.mysql_init import MySQLHandler

ids = []
removed_folder = r"D:\Users\Documents\预设\removed"


def move_folder(old_path):
    old_path = Path(old_path)
    if not old_path.exists():
        print(f"File not found: {old_path}")
        return

    remove_folder = Path(removed_folder)
    folder_name = old_path.name
    new_path = remove_folder / folder_name
    shutil.move(str(old_path), str(new_path))


def main():
    mysql_handler = MySQLHandler(host='localhost', user='root', password='Lx284190056', database='local')
    result = mysql_handler.query_data("SELECT id,raw_hash, file_path, file_name FROM file WHERE raw_hash IN (    SELECT raw_hash    FROM file    GROUP BY raw_hash    HAVING COUNT(*) > 1)ORDER BY raw_hash, id;")

    # 使用 defaultdict 创建一个以 raw_hash 为键的字典
    grouped_result = defaultdict(list)
    # 将查询结果按照 raw_hash 分组
    for row in result:
        id, raw_hash, file_path, file_name = row
        grouped_result[raw_hash].append((id, raw_hash, file_path, file_name))

    def move_file_and_append_id(path, file_id):
        move_folder(path)
        ids.append(file_id)

    for hash_value, file_info_list in grouped_result.items():
        f1_id, f1_raw_hash, f1_file_path, f1_file_name = file_info_list[0]
        f2_id, f2_raw_hash, f2_file_path, f2_file_name = file_info_list[1]

        b1 = has_brackets(f1_file_name)
        b2 = has_brackets(f2_file_name)

        if (not b1 and not b2) or (b1 and b2):
            move_file_and_append_id(f2_file_path, f2_id)
        elif b1:
            move_file_and_append_id(f1_file_path, f1_id)
        elif b2:
            move_file_and_append_id(f2_file_path, f2_id)


def has_brackets(string):
    pattern = re.compile(r'\(.\)')  # 使用正则表达式，\( 匹配左括号，. 匹配任意字符，\) 匹配右括号
    return bool(re.search(pattern, string))


if __name__ == '__main__':
    print()
    main()
    with open('data.txt', 'w') as file:
        # 将列表中的每个元素转换为字符串，并使用逗号连接
        ids_str = ', '.join(map(str, ids))
        # 将生成的字符串插入到 SQL 查询中
        query = f"DELETE FROM file\nWHERE id in ({ids_str});"
        # 写入文件
        file.write(query)
    print(len(ids))
