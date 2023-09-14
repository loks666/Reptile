import os

# 文件夹路径
folder_path = "F:/BaiduNetdiskDownload/圆周率小数点后250亿位"
# 相差数量：每个文件相隔一亿位，计算时即相差99999999
difference = 99999999
# 开始坐标，即从小数点后第一位开始计算
start_index = 1
print()


def main():
    global start_index
    # 生日
    birth_day = "19980718"
    print("您的生日为：" + birth_day)
    # 获取第一个文件名
    file_name = get_file_name(start_index, start_index + difference)
    # 获取文件路径
    file_path = get_path(file_name)

    while os.path.exists(file_path):
        if read_file(file_path, birth_day):
            break
        # 计算下一组文件的起始坐标和结束坐标
        start_index += difference + 1
        file_name = get_file_name(start_index, start_index + difference)
        file_path = get_path(file_name)


def read_file(file_path, birth_day):
    with open(file_path, 'r') as file:
        file_content = file.read()

    # 查找生日在文件内容中的位置
    print_index = file_content.find(birth_day)
    while print_index != -1:
        # 计算圆周率中生日所在的位数
        result_index = start_index + print_index
        print(birth_day + " 位于圆周率第 " + convert_to_units(result_index) + " 位!")
        print("圆周率第 " + str(result_index) + " 位的值为：" + file_content[print_index: print_index + 8] + "\n")
        # 继续查找下一个生日的位置
        print_index = file_content.find(birth_day, print_index + 1)
        # 如果想只计算一次，把下面的注释打开即可
        # return True
    return False


def get_path(file_name):
    # 拼接文件路径
    return os.path.join(folder_path, file_name)


def get_file_name(start_index, end_index):
    # 获取文件名，使用字符串格式化
    return "圆周率小数点后{0:011d}到{1:011d}一共1亿位.txt".format(start_index, end_index)


def convert_to_units(number):
    units = [100000000, 10000, 1]
    unit_names = ["亿", "万", ""]

    result = []
    for unit, unit_name in zip(units, unit_names):
        # 处理亿、万和个位之后的数字
        unit_value = number // unit
        if unit_value > 0:
            result.append("{0}{1}".format(unit_value, unit_name))
        number %= unit

    # 拼接结果字符串
    return ''.join(result)


if __name__ == "__main__":
    main()
