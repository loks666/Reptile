import os
import re
import shutil

from bs4 import BeautifulSoup


def replace_invalid_chars_in_xmp(folder_path):
    # Windows系统中不允许在文件名中使用的字符
    invalid_chars = r'[<>:"/\\|?*]'

    # 编译正则表达式，用于匹配crs:Name标签
    crs_name_pattern = re.compile(
        r'<crs:Name>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.+?)</rdf:li>\s*</rdf:Alt>\s*</crs:Name>', re.DOTALL)

    # 遍历文件夹中的所有文件
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith('.xmp'):  # 只处理.xmp文件
                file_path = os.path.join(root, file_name)
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # 查找crs:Name标签
                matches = crs_name_pattern.findall(content)
                if matches:
                    for match in matches:
                        # 检查是否包含不允许的字符
                        if re.search(invalid_chars, match):
                            # 替换不允许的字符为下划线
                            new_match = re.sub(invalid_chars, '_', match)
                            # 替换文件中的内容
                            content = content.replace(match, new_match)
                            # 回写文件
                            with open(file_path, 'w', encoding='utf-8') as file:
                                file.write(content)

    print("处理完成。")


def organize_files_by_group(folder_path):
    # 编译正则表达式，用于匹配crs:Group标签
    group_pattern = re.compile(
        r'<crs:Group>\s*<rdf:Alt>\s*<rdf:li xml:lang="x-default">(.+?)</rdf:li>\s*</rdf:Alt>\s*</crs:Group>', re.DOTALL)

    # 创建一个字典来存储组名和文件列表的映射
    group_to_files = {}

    # 遍历文件夹中的所有文件
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith('.xmp'):  # 只处理.xmp文件
                file_path = os.path.join(root, file_name)
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # 查找crs:Group标签
                match = group_pattern.search(content)
                if match:
                    group_name = match.group(1)
                    # 如果组名中包含不允许的文件夹字符，则替换为下划线
                    group_name = re.sub(r'[<>:"/\\|?*]', '_', group_name)
                    # 将文件添加到对应组名的列表中
                    if group_name not in group_to_files:
                        group_to_files[group_name] = []
                    group_to_files[group_name].append(file_path)

    # 根据组名创建文件夹并移动文件
    for group_name, files in group_to_files.items():
        # 移除组名末尾的空格
        group_name = group_name.strip()
        group_folder = os.path.join(folder_path, group_name)
        if not os.path.exists(group_folder):
            os.makedirs(group_folder)
        for file_path in files:
            # 生成目标文件路径
            destination_file_path = os.path.join(group_folder, os.path.basename(file_path))
            # 移动文件
            shutil.move(file_path, destination_file_path)

    print("文件组织完成。")


def clear_and_copy_folder(src_folder_name, dst_folder):
    # 固定的路径前缀
    prefix_path = r'D:\Users\Documents\预设\格式化文件'

    # 拼接完整的源文件夹和目标文件夹路径
    src_folder = os.path.join(prefix_path, src_folder_name)

    # 删除目标文件夹（如果存在）
    if os.path.exists(dst_folder):
        shutil.rmtree(dst_folder)
        print(f"已删除文件夹：{dst_folder}")

    # 复制源文件夹到目标位置并重命名
    shutil.copytree(src_folder, dst_folder)
    print(f"已从 {src_folder} 复制并重命名为 {dst_folder}")


def process_xmp_files(folder_path, dest_path):
    # 遍历文件夹下的所有xmp文件
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.xmp'):
            file_path = os.path.join(folder_path, file_name)

            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # 解析文件内容
            soup = BeautifulSoup(content, 'xml')
            groups = soup.find_all('crs:Group')

            # 根据crs:Group标签的数量和内容进行处理
            if len(groups) == 0:
                # 如果没有group标签，则将文件移动到目标路径
                shutil.move(file_path, os.path.join(dest_path, file_name))
            elif len(groups) > 1:
                # 如果有两个以上的group标签
                for group in groups:
                    li = group.find('rdf:li', {'xml:lang': 'x-default'})
                    if li and not li.text:
                        # 如果找到空的rdf:li标签，删除整个crs:Group
                        group.decompose()

                # 写回修改后的内容
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(str(soup))


def move_folders_without_chinese(folder_path, dest_folder):
    chinese_char_pattern = re.compile(r'[\u4e00-\u9fff]+')

    # 确保目标文件夹存在
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)

        if os.path.isdir(item_path) and not chinese_char_pattern.search(item):
            dest_path = os.path.join(dest_folder, item)
            shutil.move(item_path, dest_path)
            print(f"Moved folder: {item_path} to {dest_path}")
    return dest_folder


def move_files_and_modify_content(dest_folder, replacement_text):
    target_folder = r'D:\Users\Documents\预设\格式化文件\abroad'
    chinese_char_pattern = re.compile(r'[\u4e00-\u9fff]+')

    # 确保目标文件夹存在
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for root, dirs, files in os.walk(dest_folder):
        for item in files:
            item_path = os.path.join(root, item)
            print(f"Processing file: {item_path}")  # 输出当前处理的文件路径

            if chinese_char_pattern.search(item):
                shutil.move(item_path, os.path.join(target_folder, item))
            else:
                try:
                    with open(item_path, 'r', encoding='utf-8') as file:  # 尝试使用UTF-8编码读取
                        content = file.read()
                        soup = BeautifulSoup(content, 'xml')  # 使用'xml'作为解析器

                    # 查找所有rdf:li标签并替换文本
                    tags_modified = False
                    for tag in soup.find_all('rdf:li', {"xml:lang": "x-default"}):
                        tag.string = replacement_text
                        tags_modified = True

                    # 如果发生了修改，则写回文件
                    if tags_modified:
                        with open(item_path, 'w', encoding='utf-8') as file:  # 尝试使用UTF-8编码写入
                            file.write(str(soup))
                            print(f"Modified file: {item_path}")  # 输出修改过的文件路径
                except UnicodeDecodeError as e:
                    print(f"Error decoding file {item_path}: {e}")  # 输出解码错误信息
                except Exception as e:
                    print(f"An error occurred: {e}")  # 输出其他错误信息

    # 重命名最顶层文件夹
    current_folder_name = os.path.basename(dest_folder)
    if current_folder_name != replacement_text:
        parent_dir = os.path.dirname(dest_folder)
        new_folder_path = os.path.join(parent_dir, replacement_text)
        if not os.path.exists(new_folder_path):  # 确保不会重命名到已存在的文件夹
            os.rename(dest_folder, new_folder_path)


def move_files_and_remove_content(dest_folder):
    target_folder = r'D:\Users\Documents\预设\格式化文件\abroad'
    chinese_char_pattern = re.compile(r'[\u4e00-\u9fff]+')

    # 确保目标文件夹存在
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    for root, dirs, files in os.walk(dest_folder):
        for item in files:
            item_path = os.path.join(root, item)
            print(f"Processing file: {item_path}")  # 输出当前处理的文件路径

            if chinese_char_pattern.search(item):
                shutil.move(item_path, os.path.join(target_folder, item))
            else:
                try:
                    with open(item_path, 'r', encoding='utf-8') as file:  # 尝试使用UTF-8编码读取
                        content = file.read()
                        soup = BeautifulSoup(content, 'xml')  # 使用'xml'作为解析器

                    # 获取不包含扩展名的文件名
                    file_name_without_extension = os.path.splitext(item)[0]

                    # 替换<crs:name>下的<rdf:li xml:lang="x-default">内容为文件名
                    name_tag = soup.find('crs:name')
                    if name_tag:
                        name_li_tag = name_tag.find('rdf:li', {"xml:lang": "x-default"})
                        if name_li_tag:
                            name_li_tag.string = file_name_without_extension

                    # 清空<crs:shortname>、<crs:sortname>和<crs:description>标签下的<rdf:li xml:lang="x-default">内容
                    for tag_name in ['crs:shortname', 'crs:sortname', 'crs:description']:
                        tag = soup.find(tag_name)
                        if tag:
                            li_tag = tag.find('rdf:li', {"xml:lang": "x-default"})
                            if li_tag:
                                li_tag.string = ""

                    # 写回文件
                    with open(item_path, 'w', encoding='utf-8') as file:  # 尝试使用UTF-8编码写入
                        file.write(str(soup))
                        print(f"Modified file: {item_path}")  # 输出修改过的文件路径
                except UnicodeDecodeError as e:
                    print(f"Error decoding file {item_path}: {e}")  # 输出解码错误信息
                except Exception as e:
                    print(f"An error occurred: {e}")  # 输出其他错误信息


def process_xmp_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith('.xmp'):
                file_path = os.path.join(root, file_name)
                print(f"Processing file: {file_path}")

                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                soup = BeautifulSoup(content, 'xml')

                # 查找所有的<crs:group>标签
                group_tags = soup.find_all('crs:group')
                group_to_keep = None

                # 检查<crs:group>标签的数量和内容
                for group_tag in group_tags:
                    group_text = group_tag.find('rdf:li', {"xml:lang": "x-default"}).get_text(strip=True)
                    if group_text == "国外摄影师":
                        if group_to_keep is None:
                            group_to_keep = group_tag
                        else:
                            group_tag.decompose()
                    else:
                        group_tag.decompose()

                # 移除所有空的rdf:li标签
                for empty_li in soup.find_all('rdf:li', string=lambda text: text in (None, '')):
                    empty_li.decompose()

                # 写回修改后的内容到文件
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(str(soup))
                    print(f"Updated file: {file_path}")


def fix_empty_li_tags(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.lower().endswith('.xmp'):
                file_path = os.path.join(root, file_name)
                print(f"Processing file: {file_path}")

                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                soup = BeautifulSoup(content, 'xml')

                # 查找<crs:shortname>标签下的<rdf:alt>标签
                shortname_tags = soup.find_all('crs:shortname')
                for shortname_tag in shortname_tags:
                    alt_tag = shortname_tag.find('rdf:alt')
                    if alt_tag:
                        li_tags = alt_tag.find_all('rdf:li')
                        # 如果<rdf:li>标签存在
                        if li_tags:
                            for li_tag in li_tags:
                                # 如果是空标签，则替换为自闭合形式
                                if li_tag.get_text(strip=True) == '':
                                    li_tag.clear()
                                    li_tag.attrs['xml:lang'] = "x-default"
                                    li_tag.attrs['rdf:parseType'] = "Literal"
                        # 如果不包含<rdf:li>标签，则添加自闭合形式的<rdf:li>
                        else:
                            new_li = soup.new_tag('rdf:li', **{'xml:lang': "x-default", 'rdf:parseType': "Literal"})
                            alt_tag.append(new_li)

                # 写回修改后的内容到文件
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(str(soup))
                    print(f"Updated file: {file_path}")


def update_group_and_rename_folders(folder_path, replace_string):
    folders_to_rename = set()

    # 遍历文件夹中的所有文件
    for root, dirs, files in os.walk(folder_path):
        for i, file_name in enumerate(files):
            total = len(files)
            # print(f"处理文件： {i + 1} / {total}: {file_name}")
            if file_name.lower().endswith('.xmp'):
                file_path = os.path.join(root, file_name)
                # print(f"Processing file: {file_path}")

                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # 解析XMP文件
                soup = BeautifulSoup(content, 'xml')

                # 查找<crs:Group>标签下的<rdf:Alt>标签下的<rdf:li>标签
                group_tags = soup.find_all('crs:Group')
                for group_tag in group_tags:
                    alt_tag = group_tag.find('rdf:Alt')
                    if alt_tag:
                        li_tag = alt_tag.find('rdf:li')
                        if li_tag and replace_string in li_tag.text:
                            # 删除替换字符
                            new_text = li_tag.text.replace(replace_string, '')
                            li_tag.string.replace_with(new_text)

                            # 标记需要重命名的文件夹
                            folders_to_rename.add(root)

                            # 回写文件
                            with open(file_path, 'w', encoding='utf-8') as file:
                                file.write(str(soup))
                                # print(f"Updated file: {file_path}")

    # 重命名文件夹
    for folder in folders_to_rename:
        new_folder_name = os.path.basename(folder).replace(replace_string, '')
        new_folder_path = os.path.join(os.path.dirname(folder), new_folder_name)
        if not os.path.exists(new_folder_path):  # 检查新路径是否存在
            os.rename(folder, new_folder_path)
            # print(f"Renamed folder from '{folder}' to '{new_folder_path}'")
        else:
            pass
            # print(f"Cannot rename '{folder}' because '{new_folder_path}' already exists.")


def update_group_and_folder_names(folder_path, target_string, replacement_string):
    folders_to_rename = set()

    # 遍历文件夹中的所有文件
    for root, dirs, files in os.walk(folder_path):
        # 如果文件夹名不包含目标字符串，跳过
        if target_string not in os.path.basename(root):
            continue

        for file_name in files:
            if file_name.lower().endswith('.xmp'):
                file_path = os.path.join(root, file_name)
                # print(f"Processing file: {file_path}")

                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # 解析XMP文件
                soup = BeautifulSoup(content, 'xml')

                # 查找<crs:Group>标签
                group_tags = soup.find_all('crs:Group')
                for group_tag in group_tags:
                    # 查找<rdf:Alt>标签下的<rdf:li>标签
                    alt_tag = group_tag.find('rdf:Alt')
                    if alt_tag:
                        li_tag = alt_tag.find('rdf:li')
                        if li_tag and target_string in li_tag.text:
                            # 替换文本
                            new_text = li_tag.text.replace(target_string, replacement_string)
                            li_tag.string.replace_with(new_text)

                            # 标记需要重命名的文件夹
                            folders_to_rename.add(root)

                # 回写文件
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(str(soup))
                    # print(f"Updated file: {file_path}")

    # 重命名文件夹
    for folder in folders_to_rename:
        new_folder_name = os.path.basename(folder).replace(target_string, replacement_string)
        new_folder_path = os.path.join(os.path.dirname(folder), new_folder_name)
        if not os.path.exists(new_folder_path):  # 检查新路径是否存在
            os.rename(folder, new_folder_path)
            # print(f"Renamed folder from '{folder}' to '{new_folder_path}'")
        else:
            pass
            # print(f"Cannot rename '{folder}' because '{new_folder_path}' already exists.")


def remove_duplicate_files(source_folder, removed_folder):
    # 确保移除的文件夹存在
    if not os.path.exists(removed_folder):
        os.makedirs(removed_folder)

    # 遍历文件夹中的所有文件
    for file_name in os.listdir(source_folder):
        print(file_name)
        # 获取文件名和扩展名
        base_name, extension = os.path.splitext(file_name)

        # 检查文件名最后三个字符是否为'(1)'
        if base_name.endswith('(1)'):
            # 移除文件名中的'(1)'
            new_base_name = base_name[:-3]
            new_file_name = new_base_name + extension

            # 构建新旧文件的完整路径
            old_file_path = os.path.join(source_folder, file_name)
            new_file_path = os.path.join(source_folder, new_file_name)
            removed_file_path = os.path.join(removed_folder, file_name)

            # 检查去掉'(1)'后是否存在重名文件
            if os.path.exists(new_file_path):
                # 存在重名文件，移动带有'(1)'的文件到removed文件夹
                shutil.move(old_file_path, removed_file_path)
                print(f"Moved duplicate file '{old_file_path}' to '{removed_file_path}'")
            else:
                os.rename(old_file_path, new_file_path)


def update_xmp_tags_and_rename_files(folder_path, target_string, replacement_string):
    # 遍历文件夹中的所有文件
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if target_string not in file_name:
                continue
            # 检查文件是否为XMP文件
            if file_name.lower().endswith('.xmp'):
                file_path = os.path.join(root, file_name)
                # print(f"Processing XMP file: {file_path}")

                # 读取XMP文件内容
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                # 解析XMP文件
                soup = BeautifulSoup(content, 'xml')

                # 查找所有<crs:Name>标签
                name_tags = soup.find_all('crs:Name')
                file_renamed = False  # 标记文件是否需要重命名
                for name_tag in name_tags:
                    # 在每个<crs:Name>标签中查找<rdf:Alt>标签
                    alt_tag = name_tag.find('rdf:Alt')
                    if alt_tag:
                        # 在<rdf:Alt>标签中查找<rdf:li>标签
                        li_tag = alt_tag.find('rdf:li')
                        if li_tag and target_string in li_tag.text:
                            # 替换<rdf:li>标签的内容
                            li_tag.string = li_tag.text.replace(target_string, replacement_string)
                            file_renamed = True  # 需要重命名文件

                # 将修改后的XML内容写回文件
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(str(soup))

                # 如果需要重命名文件，则重命名XMP文件
                if file_renamed:
                    new_file_name = file_name.replace(target_string, replacement_string)
                    new_file_path = os.path.join(root, new_file_name)
                    os.rename(file_path, new_file_path)
                    print(f"Renamed file: {file_path} to {new_file_path}")


if __name__ == '__main__':
    print()
    # 设置文件夹路径
    folder_path = r'D:\Users\Documents\预设\格式化文件\xmp'
    # 设置文件夹名
    src_folder_name = 'xmp - Copy'

    # 调用函数执行操作
    clear_and_copy_folder(src_folder_name, folder_path)
    # 调用方法
    replace_invalid_chars_in_xmp(folder_path)
    organize_files_by_group(folder_path)
    # 处理group标签
    # 定义文件夹路径
    dest_path = r'D:\Users\Documents\预设\格式化文件\xmp'
    dest_folder = r'D:\Users\Documents\预设\removed'
    move_folders_without_chinese(folder_path, dest_folder)
    move_files_and_modify_content(r'D:\Users\Documents\预设\格式化文件\国外摄影师', "国外摄影师")
    move_files_and_remove_content(r'D:\Users\Documents\预设\格式化文件\国外摄影师')
    process_xmp_files(r'D:\Users\Documents\预设\格式化文件\国外摄影师')
    fix_empty_li_tags(r'D:\Users\Documents\预设\格式化文件\国外摄影师')
    folder_path = r'D:\Users\Documents\预设\格式化文件\飞林预设'
    update_group_and_folder_names(folder_path, 'lrtemplate', '飞林预设')
    removed = r'D:\Users\Documents\预设\格式化文件\removed'
    remove_duplicate_files(folder_path, removed)
    update_group_and_folder_names(folder_path, '-xmp', '飞林预设')
    os.system("shutdown /s /t 1")
    remove_duplicate_files(folder_path, dest_folder)
    update_xmp_tags_and_rename_files(folder_path, '[]', '')

