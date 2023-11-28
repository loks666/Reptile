import os
import re
import shutil

from bs4 import BeautifulSoup

file_folder = r'D:\Users\Documents\预设\格式化文件\num'
print()


def remove_name_group(patterns):
    for root, dirs, files in os.walk(file_folder):
        for file_name in files:
            if file_name.endswith('.xmp'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # 使用正则表达式删除 <crs:Name> 和 <crs:Group> 标签及其内容
                for pattern in patterns:
                    content = re.sub(pattern, '', content, flags=re.DOTALL)

                # 写回文件
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(content)


def rename():
    for root, dirs, files in os.walk(r"D:\Users\Documents\预设\格式化文件\xmp\all_not\飞林预设"):
        for file_name in files:
            if file_name.endswith('.xmp'):
                file_path = os.path.join(root, file_name)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                    # 使用正则表达式匹配 <crs:Name> 和 <crs:Group> 中的内容
                    name_match = re.search(r'<crs:Name>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.*?)</rdf:li>',
                                           content,
                                           re.DOTALL)
                    group_match = re.search(r'<crs:Group>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.*?)</rdf:li>',
                                            content,
                                            re.DOTALL)

                    # 获取匹配到的内容
                    c_name = name_match.group(1).strip() if name_match else None
                    c_group = group_match.group(1).strip() if group_match else None

                    # 使用文件名替换匹配到的内容
                    new_content = content.replace(c_name, file_name.split('.')[0])

                # 将修改后的内容写回文件
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(new_content)

                print(f"{file_name}: {c_name} -> {file_name.split('.')[0]}")


def add_name_group(c_group):
    # 遍历文件夹下的所有文件
    for filename in os.listdir(file_folder):
        file_path = os.path.join(file_folder, filename)

        # 检查是否为文件
        if os.path.isfile(file_path):
            # 获取文件名（去除后缀）
            file_name = os.path.splitext(filename)[0]

            # 分割文件名，得到c_name和c_group
            c_name = file_name.strip()

            # 去除c_group中的空格
            print(c_name + "," + c_group)
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()

            # 检查文件内容是否包含"</rdf:Description>"
            if "</rdf:Description>" in file_content:
                # 在匹配行之前插入新的文本
                match = re.search(r'</rdf:Description>', file_content)
                if match:
                    insert_position = match.start()
                    new_content = (
                        f'<crs:Name>\n'
                        f'    <rdf:Alt>\n'
                        f'        <rdf:li xml:lang="x-default">{c_name}</rdf:li>\n'
                        f'    </rdf:Alt>\n'
                        f'</crs:Name>\n'
                        f'<crs:Group>\n'
                        f'    <rdf:Alt>\n'
                        f'        <rdf:li xml:lang="x-default">{c_group}</rdf:li>\n'
                        f'    </rdf:Alt>\n'
                        f'</crs:Group>\n'
                    )
                    new_file_content = file_content[:insert_position] + new_content + file_content[insert_position:]

                    # 写回文件
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(new_file_content)
            else:
                print(f"文件内容不包含</rdf:Description>: {file_path}")


def add_group(c_group):
    # 遍历文件夹下的所有文件
    for filename in os.listdir(file_folder):
        file_path = os.path.join(file_folder, filename)

        # 检查是否为文件
        if os.path.isfile(file_path):
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()

            # 检查文件内容是否包含"</rdf:Description>"
            if "</rdf:Description>" in file_content:
                # 在匹配行之前插入新的文本
                match = re.search(r'</rdf:Description>', file_content)
                if match:
                    insert_position = match.start()
                    new_content = (
                        f'<crs:Group>\n'
                        f'    <rdf:Alt>\n'
                        f'        <rdf:li xml:lang="x-default">{c_group}</rdf:li>\n'
                        f'    </rdf:Alt>\n'
                        f'</crs:Group>\n'
                    )
                    new_file_content = file_content[:insert_position] + new_content + file_content[insert_position:]

                    # 写回文件
                    with open(file_path, 'w', encoding='utf-8') as file:
                        file.write(new_file_content)
            else:
                print(f"文件内容不包含</rdf:Description>: {file_path}")


def remove_label():
    patterns = [
        r'<crs:Name>.*?</crs:Name>',
        r'<crs:Group>.*?</crs:Group>'
    ]

    remove_name_group(patterns)


def clean_filename(filename):
    # 替换不支持的字符
    invalid_chars = ['|', ':', '\\', '/', '*', '?', '"', '<', '>', '.']
    for char in invalid_chars:
        filename = filename.replace(char, '-')
    return filename


def update_c_name_tag(file_path, new_c_name):
    with open(file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()

    # 使用BeautifulSoup解析XML内容
    soup = BeautifulSoup(file_content, 'xml')
    c_name_tag = soup.find('rdf:li', {'xml:lang': 'x-default'})

    if c_name_tag:
        # 更新标签内容
        c_name_tag.string = new_c_name

        # 写回文件
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(str(soup))


def c_name_to_file_name():
    # 创建目录，如果不存在
    duplication_folder = r'D:\Users\Documents\预设\格式化文件\xmp\duplication_name'
    os.makedirs(duplication_folder, exist_ok=True)

    # 遍历文件夹下的所有文件
    for filename in os.listdir(file_folder):
        if filename.endswith('.xmp'):
            file_path = os.path.join(file_folder, filename)

            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()

            # 使用BeautifulSoup解析XML内容
            soup = BeautifulSoup(file_content, 'xml')
            c_name_tag = soup.find('rdf:li', {'xml:lang': 'x-default'})

            if c_name_tag:
                c_name = c_name_tag.text.strip()

                # 清理文件名
                cleaned_filename = clean_filename(c_name)
                print(filename, cleaned_filename)

                # 构建新文件名，如果文件名已经等于标签中的内容，就不修改
                if filename == f"{cleaned_filename}.xmp":
                    continue
                else:
                    new_file_name = f"{cleaned_filename}.xmp"

                    # 构建新文件路径
                    new_file_path = os.path.join(file_folder, new_file_name)

                    # 如果新文件名已存在，移动文件到重复的文件夹
                    if os.path.exists(new_file_path):
                        new_file_path_duplicated = os.path.join(duplication_folder, f"{new_file_name}")
                        shutil.move(file_path, new_file_path_duplicated)
                        print(f"文件名已存在，移动文件: {file_path} -> {new_file_path_duplicated}")
                    else:
                        # 重命名文件
                        os.rename(file_path, new_file_path)
                        print(f"重命名文件: {file_path} -> {new_file_path}")

                        # 更新标签内容
                        update_c_name_tag(new_file_path, cleaned_filename)


def find_file_name():
    import os
    import shutil

    file_folder = r'D:\Users\Documents\预设\格式化文件\xmp\c_name'
    output_folder = r'D:\Users\Documents\预设\格式化文件\xmp\num'

    # 创建目录，如果不存在
    os.makedirs(output_folder, exist_ok=True)

    # 获取文件夹下的所有文件
    all_files = os.listdir(file_folder)

    # 根据文件名的开头是否为数字来筛选文件
    numeric_files = [filename for filename in all_files if filename[0].isdigit()]

    # 将符合条件的文件移动到 "num" 文件夹下
    for filename in numeric_files:
        source_path = os.path.join(file_folder, filename)
        destination_path = os.path.join(output_folder, filename)
        shutil.move(source_path, destination_path)
        print(f'移动文件: {source_path} -> {destination_path}')




if __name__ == '__main__':
    add_group("俄罗斯灰调(长风素材)")
    # find_file_name()
    # c_name_to_file_name()
    # add_name_group("rkrkrk") # 添加组名
