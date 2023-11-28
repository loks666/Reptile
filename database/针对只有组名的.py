import shutil

from bs4 import BeautifulSoup
from xlrd.xlsx import ET

from database.mysql_init import MySQLHandler

print()


def group_file_created_folder(sql):
    mysql_handler = MySQLHandler(host='localhost', user='root', password='Lx284190056', database='local')
    result = mysql_handler.query_data(sql)
    for row in result:
        id, filename, raw_hash, file_path, c_name, c_group, content, new_hash = row

        # print(filename, file_path)

        # 获取文件所在的文件夹路径
        folder_path = os.path.dirname(file_path)

        # 构建新文件夹路径
        if c_group is None:
            print(sql, "c_group is None!")
            return
        new_folder_path = os.path.join(folder_path, c_group)

        # 如果文件夹不存在，则创建
        os.makedirs(new_folder_path, exist_ok=True)

        # 构建新路径
        new_path = os.path.join(new_folder_path, filename)
        # print(new_path + '\n')

        # 移动文件
        shutil.move(file_path, new_path)


def add_group(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.xmp'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = file.readlines()

                for i, line in enumerate(file_content):
                    if '</crs:Name>' in line:
                        # 插入Group标签内容
                        c_group = os.path.basename(root)
                        group_content = (
                            f'   <crs:Group>\n'
                            f'       <rdf:Alt>\n'
                            f'           <rdf:li xml:lang="x-default">{c_group}</rdf:li>\n'
                            f'       </rdf:Alt>\n'
                            f'   </crs:Group>\n'
                        )
                        file_content.insert(i + 1, group_content)

                # 将修改后的内容写回文件
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.writelines(file_content)


def get_group(content):
    group_match = re.search(r'<crs:Group>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.*?)</rdf:li>', content,
                            re.DOTALL)
    # 设置默认值
    c_group = None
    if group_match is not None:
        c_group = group_match.group(1).strip()
    return c_group


def update_name_and_content(string, file):
    # 读取文件内容
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 根据传入的文本重命名文件名和文件name标签内容
    name_match = re.search(r'<crs:Name>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.*?)</rdf:li>', content,
                           re.DOTALL)
    # 设置默认值
    c_name = None

    if name_match is not None:
        c_name = name_match.group(1).strip()
        # 替换<crs:Name>标签内容
        content = re.sub(
            r'<crs:Name>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.*?)</rdf:li>\s*</rdf:Alt>\s*</crs:Name>',
            f'<crs:Name><rdf:Alt><rdf:li xml:lang="x-default">{string}</rdf:li></rdf:Alt></crs:Name>',
            content, flags=re.DOTALL)
    # 更新文件名
    if c_name is not None:
        # 获取文件名和扩展名
        file_name, file_ext = os.path.splitext(file)
        # 构造新的文件名
        new_file_name = f'{string}{file_ext}'
        # 重命名文件
        os.rename(file, os.path.join(os.path.dirname(file), new_file_name))

    # 写入更新后的内容
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)


def update_group_and_content(string, file):
    # 打开文件并读取内容
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 根据传入的文本更新文件内容
    updated_content = re.sub(r'<crs:Group>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.*?)</rdf:li>',
                             '<crs:Group>\n<rdf:Alt>\n<rdf:li xml:lang="x-default">' + string + '</rdf:li>',
                             content, flags=re.DOTALL)

    # 将更新后的内容写入文件
    with open(file, 'w', encoding='utf-8') as f:
        f.write(updated_content)


def rename_and_update_content(path):
    # 遍历指定目录下的所有文件夹和文件
    for root, dirs, files in os.walk(path):
        for i, file in enumerate(files):
            if file.endswith('.xmp'):
                # 生成新的文件名
                new_filename = os.path.basename(root) + '_' + str(i + 1) + '.xmp'
                # 构造文件的完整路径
                file_path = os.path.join(root, file)
                new_file_path = os.path.join(root, new_filename)

                # 更新文件名和文件内容
                update_name_and_content(new_filename, file_path)
                os.rename(file_path, new_file_path)


def only_update_content(path):
    # 遍历指定目录下的所有文件夹和文件
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.xmp'):
                # 构造文件的完整路径
                file_path = os.path.join(root, file)

                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 获取文件名和扩展名
                file_name, file_ext = os.path.splitext(file)

                # 更新文件内容
                content = re.sub(
                    r'<crs:Name>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.*?)</rdf:li>\s*</rdf:Alt>\s*</crs:Name>',
                    f'<crs:Name><rdf:Alt><rdf:li xml:lang="x-default">{file_name}</rdf:li></rdf:Alt></crs:Name>',
                    content, flags=re.DOTALL)

                # 写入更新后的内容
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)


def update_name_tag(folder):
    # 遍历文件夹下的所有文件
    for root, dirs, files in os.walk(folder):
        for file in files:
            # 只处理扩展名为 .xmp 的文件
            if os.path.splitext(file)[1] == '.xmp':
                file_path = os.path.join(root, file)
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 获取文件名（不含扩展名）
                file_name = os.path.splitext(os.path.basename(file_path))[0]

                # 更新 crs:Name 标签内容
                content = re.sub(
                    r'<crs:Name>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.*?)</rdf:li>\s*</rdf:Alt>\s*</crs:Name>',
                    f'<crs:Name><rdf:Alt><rdf:li xml:lang="x-default">{file_name}</rdf:li></rdf:Alt></crs:Name>',
                    content, flags=re.DOTALL)

                # 写入更新后的内容
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)


def rename_folders_and_files(folder, string):
    """
    去掉文件夹和文件名中的字符，并更新 xmp 文件中的 crs:Name 和 crs:Group 标签内容
    """
    # 遍历文件夹下的所有文件和文件夹
    for root, dirs, files in os.walk(folder):
        # 处理文件夹
        for dir_name in dirs:
            if string in dir_name:
                # 获取新的文件夹名
                new_dir_name = dir_name.replace(string, '')
                # 重命名文件夹
                os.rename(os.path.join(root, dir_name), os.path.join(root, new_dir_name))

        # 处理文件
        for file in files:
            if string in file:
                # 获取新的文件名
                new_file_name = os.path.splitext(file)[0].replace(string, '') + os.path.splitext(file)[1]
                # 重命名文件
                os.rename(os.path.join(root, file), os.path.join(root, new_file_name))

    # 遍历文件夹下的所有文件和文件夹
    for root, dirs, files in os.walk(folder):
        # 处理文件夹中的 xmp 文件
        for dir_name in dirs:
            dirs = os.path.join(root, dir_name)
            for file in os.listdir(dirs):
                if file.endswith('.xmp'):
                    file_path = os.path.join(root, dir_name, file)
                    # 读取文件内容
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # 获取文件名（不含扩展名）
                    file_name = os.path.splitext(file)[0].replace(string, '')

                    # 更新 crs:Name 标签内容
                    content = re.sub(
                        r'<crs:Name>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.*?)</rdf:li>\s*</rdf:Alt>\s*</crs:Name>',
                        f'<crs:Name><rdf:Alt><rdf:li xml:lang="x-default">{file_name}</rdf:li></rdf:Alt></crs:Name>',
                        content, flags=re.DOTALL)

                    # 更新 crs:Group 标签内容
                    content = re.sub(
                        r'<crs:Group>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.*?)</rdf:li>\s*</rdf:Alt>\s*</crs:Group>',
                        f'<crs:Group><rdf:Alt><rdf:li xml:lang="x-default">{dir_name}</rdf:li></rdf:Alt></crs:Group>',
                        content, flags=re.DOTALL)

                    # 写入更新后的内容
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)

        # 处理文件中的 xmp 文件
        for file in files:
            if file.endswith('.xmp'):
                file_path = os.path.join(root, file)
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 获取文件名（不含扩展名）
                file_name = os.path.splitext(file)[0].replace(string, '')

                # 更新 crs:Name 标签内容
                content = re.sub(
                    r'<crs:Name>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.*?)</rdf:li>\s*</rdf:Alt>\s*</crs:Name>',
                    f'<crs:Name><rdf:Alt><rdf:li xml:lang="x-default">{file_name}</rdf:li></rdf:Alt></crs:Name>',
                    content, flags=re.DOTALL)

                # 更新 crs:Group 标签内容
                dir_name = os.path.basename(root)
                content = re.sub(
                    r'<crs:Group>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.*?)</rdf:li>\s*</rdf:Alt>\s*</crs:Group>',
                    f'<crs:Group><rdf:Alt><rdf:li xml:lang="x-default">{dir_name}</rdf:li></rdf:Alt></crs:Group>',
                    content, flags=re.DOTALL)

                # 重命名文件
                os.rename(file_path, os.path.join(root, file_name + '.xmp'))

                # 写入更新后的内容
                with open(os.path.join(root, file_name + '.xmp'), 'w', encoding='utf-8') as f:
                    f.write(content)


import os
import re


def update_char_in_files(folder, find_char, replace_char):
    """
    将文件夹中所有文件和文件夹中的指定字符替换为新的字符，并更新 xmp 文件中的 crs:Name 和 crs:Group 标签内容
    """
    # 遍历文件夹下的所有文件和文件夹
    for root, dirs, files in os.walk(folder):
        # 处理文件夹
        for dir_name in dirs:
            if find_char in dir_name:
                # 获取新的文件夹名
                new_dir_name = dir_name.replace(find_char, replace_char)
                # 重命名文件夹
                os.rename(os.path.join(root, dir_name), os.path.join(root, new_dir_name))

        # 处理文件
        for file in files:
            if find_char in file:
                # 获取新的文件名
                new_file_name = file.replace(find_char, replace_char)
                # 重命名文件
                os.rename(os.path.join(root, file), os.path.join(root, new_file_name))

        # 处理文件夹中的 xmp 文件
        for dir_name in dirs:
            for file in os.listdir(os.path.join(root, dir_name)):
                if file.endswith('.xmp'):
                    file_path = os.path.join(root, dir_name, file)
                    # 读取文件内容
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # 获取文件名（不含扩展名）
                    file_name = os.path.splitext(file)[0].replace(find_char, replace_char)

                    # 更新 crs:Name 标签内容
                    content = re.sub(
                        r'<crs:Name>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.*?)</rdf:li>\s*</rdf:Alt>\s*</crs:Name>',
                        f'<crs:Name><rdf:Alt><rdf:li xml:lang="x-default">{file_name}</rdf:li></rdf:Alt></crs:Name>',
                        content, flags=re.DOTALL)

                    # 更新 crs:Group 标签内容
                    content = re.sub(
                        r'<crs:Group>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.*?)</rdf:li>\s*</rdf:Alt>\s*</crs:Group>',
                        f'<crs:Group><rdf:Alt><rdf:li xml:lang="x-default">{dir_name}</rdf:li></rdf:Alt></crs:Group>',
                        content, flags=re.DOTALL)

                    # 写入更新后的内容
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)

        # 处理文件中的 xmp 文件
        for file in files:
            if file.endswith('.xmp'):
                file_path = os.path.join(root, file)
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 获取文件名（不含扩展名）
                file_name = os.path.splitext(file)[0].replace(find_char, replace_char)

                # 更新 crs:Name 标签内容
                content = re.sub(
                    r'<crs:Name>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.*?)</rdf:li>\s*</rdf:Alt>\s*</crs:Name>',
                    f'<crs:Name><rdf:Alt><rdf:li xml:lang="x-default">{file_name}</rdf:li></rdf:Alt></crs:Name>',
                    content, flags=re.DOTALL)

                # 更新 crs:Group 标签内容
                content = re.sub(
                    r'<crs:Group>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.*?)</rdf:li>\s*</rdf:Alt>\s*</crs:Group>',
                    f'<crs:Group><rdf:Alt><rdf:li xml:lang="x-default">{os.path.dirname(file)}</rdf:li></rdf:Alt></crs:Group>',
                    content, flags=re.DOTALL)

                # 写入更新后的内容
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)


def replace_xmp_file_names(folder_path):
    """
    将文件夹中的所有 xmp 文件名替换为Name标签名
    """
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.xmp'):
                file_path = os.path.join(root, file)
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 获取文件名（不含扩展名）
                file_name = os.path.splitext(file)[0]

                # 替换 <crs:Name> 标签中的文本
                new_content = re.sub(
                    r'<crs:Name>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.*?)</rdf:li>\s*</rdf:Alt>\s*</crs:Name>',
                    f'<crs:Name><rdf:Alt><rdf:li xml:lang="x-default">{file_name}</rdf:li></rdf:Alt></crs:Name>',
                    content, flags=re.DOTALL)

                # 写入文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)


def replace_group_tag(folder_path, new_group):
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith('.xmp'):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                soup = BeautifulSoup(content, 'xml')
                for group in soup.find_all('crs:Group'):
                    for li in group.find_all('rdf:li', {'xml:lang': 'x-default'}):
                        li.string = new_group
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(str(soup))


# 调用示例
if __name__ == '__main__':
    # add_group(r'D:\Users\Documents\预设\格式化文件\xmp\c_name')
    # group_file_created_folder(
    #     "SELECT *FROM file WHERE file_path LIKE '%not%'  AND c_group IN (    SELECT c_group    FROM file    WHERE file_path LIKE '%not%'    GROUP BY c_group    HAVING COUNT(*) = 2  )ORDER BY c_group DESC ;")
    # folder_path = r'D:\Users\Documents\预设\格式化文件\xmp\not_rename\chinese'
    import os
    from bs4 import BeautifulSoup


    def process_files(directory):
        # Windows文件命名中禁止的字符
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

        for filename in os.listdir(directory):
            if filename.endswith('.xmp'):
                with open(os.path.join(directory, filename), 'r+', encoding='utf-8') as file:
                    contents = file.read()
                    soup = BeautifulSoup(contents, 'xml')
                    tags = soup.find_all('crs:Group')

                    for tag in tags:
                        for char in invalid_chars:
                            if char in tag.text:
                                tag.string = tag.text.replace(char, '_')

                    # 回写文件
                    file.seek(0)
                    file.write(str(soup))
                    file.truncate()


    # 使用方法
    process_files(r'D:\Users\Documents\预设\格式化文件\xmp')









