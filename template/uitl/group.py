import os
import shutil

# 源路径
source = "E:\\total"
# 目标路径[分类路径]
target = "E:\\group"
dirs = []


# 分类
def group_file(path):
    # 遍历当前路径下所有文件
    files = [os.path.abspath(os.path.join(r, f)) for r, _, fs in os.walk(path) for f in fs]
    type_list = []
    for f in files:
        # 字符串拼接
        # print(f)
        # name_list = f.split('.')
        name_list = os.path.splitext(f)

        # prefix = name_list[0]
        suffix = get_suffix(name_list)
        # real_url = path.join(url, f)
        # 打印出来
        # print(real_url)
        type_list.append(suffix)
    return list(set(type_list))


# 创建文件夹
def mkdir(list):
    for path in list:
        name = os.path.join(target, path)
        if not os.path.exists(name):
            os.mkdir(name)


# 移动文件
def move(path):
    files = [os.path.abspath(os.path.join(r, f)) for r, _, fs in os.walk(path) for f in fs]
    for f in files:
        name_list = f.split('.')

        # prefix = name_list[0]
        suffix = get_suffix(name_list)
        new_path = os.path.join(target, suffix, os.path.basename(f))
        print('正在移动文件：' + f)
        shutil.move(f, new_path)


def get_suffix(names):
    if is_chinese(names[len(names) - 1]):
        return 'nothing'
    else:
        return names[len(names) - 1].replace('.', '')


def is_chinese(check_str):
    """
    判断字符串中是否包含中文
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


if __name__ == '__main__':
    dirs = group_file(source)
    # for i in dirs:
    #     print(i)
    mkdir(dirs)
    move(source)
    # files = [os.path.abspath(os.path.join(r, f)) for r, _, fs in os.walk('E:\\total') for f in fs]
    # print(files)