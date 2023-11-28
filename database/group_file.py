import os
import re
import shutil


def contains_chinese(text):
    """
    判断文本中是否包含中文字符
    """
    chinese_pattern = re.compile('[\u4e00-\u9fa5]')
    return bool(chinese_pattern.search(text))


def rename_files_without_chinese(folder_path, prefix='飞林预设'):
    """
    重命名文件夹中文件名不包含中文的文件
    """
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path) and not contains_chinese(file_name):
            new_name = f'{prefix} {file_name.split(".")[0]} ({len(os.listdir(folder_path))}).{file_name.split(".")[-1]}'
            new_path = os.path.join(folder_path, new_name)

            os.rename(file_path, new_path)
            print(f'Renamed: {file_path} to {new_path}')


def group_folder(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.xmp'):
                file_path = os.path.join(root, file_name)

                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # 使用正则表达式查找<crs:Group>标签中的内容
                group_match = re.search(
                    r'<crs:Group>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.*?)</rdf:li>',
                    content, re.DOTALL
                )

                if group_match is not None:
                    c_group = group_match.group(1).strip()

                    # 构建目标文件夹路径
                    target_folder = os.path.join(folder_path, c_group)

                    # 如果目标文件夹不存在，创建它
                    if not os.path.exists(target_folder):
                        os.makedirs(target_folder)

                    # 移动文件到目标文件夹
                    target_file_path = os.path.join(target_folder, file_name)
                    shutil.move(file_path, target_file_path)


def get_files():
    for root, dirs, files in os.walk(folder_path):
        return files


def remove_name_has_one():
    source_folder = folder_path
    duplication_folder = r'D:\Users\Documents\预设\格式化文件\duplication_name'
    count = 0
    # 遍历源文件夹中的所有文件
    for filename in os.listdir(source_folder):
        source_path = os.path.join(source_folder, filename)

        # 检查文件名是否包含 "(1)"
        if "(1)" in filename:
            # 去除 "(1)" 并构建新的文件名
            new_filename = filename.replace("(1)", "").strip()

            # 构建新文件路径
            new_path = os.path.join(source_folder, new_filename)

            # 如果新文件名已存在，移动文件到重复的文件夹
            if os.path.exists(new_path):
                # 构建新的目标路径
                duplication_path = os.path.join(duplication_folder, filename)

                # 移动文件
                shutil.move(source_path, duplication_path)
                count += 1
                print(f"文件名已存在，移动文件: {source_path} -> {duplication_path}")
            else:
                pass
                # 重命名文件
                # os.rename(source_path, new_path)
                # print(f"重命名文件: {source_path} -> {new_path}")
    print(count)


def get_c_group(content):
    files = get_files()
    # 遍历文件夹下的所有文件，判断内容中是否包含 <crs:Group> 标签
    group_match = re.search(r'<crs:Group>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.*?)</rdf:li>', content,
                            re.DOTALL)
    c_group = group_match.group(1).strip() if group_match else None
    return c_group


def get_c_name(content):
    # 使用正则表达式匹配 <crs:Name> 和 <crs:Group> 中的内容
    name_match = re.search(r'<crs:Name>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.*?)</rdf:li>', content, re.DOTALL)
    # 获取匹配到的内容
    c_name = name_match.group(1).strip() if name_match else None
    return c_name


def is_valid_filename(filename):
    # 不允许的字符列表
    disallowed_characters = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

    # 判断文件名是否包含不允许的字符
    for char in filename:
        if char in disallowed_characters:
            return True
    return False


def process_files(folder_path, duplication_folder, exception_folder):
    files_list = os.listdir(folder_path)
    print("整理文件中...")
    for file_name in files_list:
        # 判断是否是 .xmp 后缀的文件
        if not file_name.endswith('.xmp'):
            continue

        # 获取文件路径
        file_path = os.path.join(folder_path, file_name)

        try:
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()

            # 获取文件名（不含后缀）
            file_name_without_extension, _ = os.path.splitext(file_name)

            # 获取 <crs:Name> 标签中的内容
            c_name = get_c_name(file_content)

            if is_valid_filename(c_name):
                # print(f"文件名无效: {c_name}")
                shutil.move(file_path, os.path.join(r"D:\Users\Documents\预设\格式化文件\not_rename", file_name))
                continue

            # 如果 <crs:Name> 中的内容和文件名相同，则不处理
            if c_name == file_name_without_extension:
                continue
            else:
                # 构建新文件路径
                new_file_name = f"{c_name}.xmp"
                new_file_path = os.path.join(folder_path, new_file_name)

                # print(new_file_path)
                # 如果新文件名已存在，移动文件到重复的文件夹
                if os.path.exists(new_file_path):
                    pass
                    # print(f"移动文件: {file_path} -> {new_file_path}")
                    duplication_file = os.path.join(duplication_folder, new_file_name)
                    shutil.move(file_path, duplication_file)
                else:
                    pass
                    # 直接重命名
                    # print(f"重命名文件: {file_path} -> {os.path.join(folder_path, new_file_name)}")
                    os.rename(file_path, os.path.join(folder_path, new_file_name))
        except UnicodeDecodeError:
            # 处理 UnicodeDecodeError 异常
            exception_file_path = os.path.join(exception_folder, file_name)
            shutil.move(file_path, exception_file_path)
            print(f"处理异常文件: {file_name} -> {exception_file_path}")


def clear_files():
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


def replace_crs_tags(directory):
    if not os.path.isdir(directory):
        print("The provided directory does not exist.")
        return

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith('.xmp'):
                file_path = os.path.join(root, filename)
                print(f"Processing file: {file_path}")  # 调试信息

                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # 替换内容
                content = content.replace('<crs:name>', '<crs:Name>')
                content = content.replace('</crs:name>', '</crs:Name>')
                content = content.replace('<crs:group>', '<crs:Group>')
                content = content.replace('</crs:group>', '</crs:Group>')

                # 保存替换后的内容
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Updated {file_path}")


if __name__ == "__main__":
    print()
    # clear_files()
    # clear_folder(r'D:\Users\Documents\预设\格式化文件\duplication_name')
    folder_path = r'D:\Users\Documents\预设\格式化文件\xmp'
    duplication_folder = r'D:\Users\Documents\预设\格式化文件\duplication_name'
    exception_folder = r'D:\Users\Documents\预设\格式化文件\duplication_name\exception'
    # process_files(folder_path, duplication_folder, folder_path)
    replace_crs_tags(r'D:\Users\Documents\预设\格式化文件')
