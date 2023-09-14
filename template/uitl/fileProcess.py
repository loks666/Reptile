import os
import shutil

# 源路径
source = "E:\\total"
# 目标路径[分类路径]
target = "E:\\group"

path = "E:\\LR预设"
path = "E:\\remove"
dirs = []


def api():
    print(os.getcwd())  # 获取当前工作目录路径
    print(os.path.abspath('.'))  # 获取当前工作目录路径
    print(os.path.abspath('test.txt'))  # 获取当前目录文件下的工作目录路径
    print(os.path.abspath('..'))  # 获取当前工作的父目录 ！注意是父目录路径
    print(os.path.abspath(os.curdir))  # 获取当前工作目录路径
    os.rename(source, target)  # 修改文件名


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
        print('正在移动文件：' + f, '新路径名：' + new_path)
        # shutil.move(f, new_path)


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


def modify(file_path):
    files = [os.path.abspath(os.path.join(r, f)) for r, _, fs in os.walk(file_path) for f in fs]
    for f in files:
        # f_name = os.path.basename(f)  # 获取文件名
        # print(f_name)
        # print(f)
        del_small_file(f)
        # os.rename(n1, n2)
    # for i in os.walk(file_path):
    #     print(i[0])  # 返回文件夹的名字，先返回第一层文件夹，然后返回文件夹内的文件夹
    # for j in i[2]:
    #     print(j)  # 输出文件的名字


def del_small_file(file_name):
    size = os.path.getsize(file_name)
    file_size = 1000 * 1024  # 更改成你想删除的界限，我这里是1000kb
    if size < file_size:
        os.remove(file_name)
        print('remove', size, file_name)
        os.system('shutdown /s /t 0')


if __name__ == '__main__':
    
    # modify(path)
    # print(os.path.getsize('E:\\remove\94704.jpg'))
    # dirs = group_file(source) #分类文件
    # dirs = {'jpg', 'mov', 'mp4'}
    # for i in dirs:
    #     print(i)
    # mkdir(dirs)
    # move(source)
    # files = [os.path.abspath(os.path.join(r, f)) for r, _, fs in os.walk('E:\\total') for f in fs]
    # print(files)
