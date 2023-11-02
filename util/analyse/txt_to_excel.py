import os
import re
import sys
import pandas as pd

# 定义文件夹路径
folder_path = "txt"
# 创建一个空的列表以存储提取的数据
extracted_data = []


# 遍历文件夹中的.txt文件
def get_data(line):
    start_index = line.find("】")
    end_index = line.find("\n")
    if start_index != -1 and end_index != -1:
        return line[start_index + 1:end_index].strip()


# 遍历所有.txt文件
for file_name in os.listdir(folder_path):
    if file_name.endswith(".txt"):
        result_path = os.path.join(folder_path, file_name)
        data = {"法规目录": '', "链接": '', "标题": '', "文件名称": file_name,
                "发布部门": '', "批准部门": '', "发文字号": '', "批准日期": '', "日期": '', "时效性": '',
                "失效依据": '', "效力级别": '', "法规类别": '', "关键词": '', "专题分类": '',
                "文件夹名称": "", "地址": file_name}

        # 打开文件并读取内容
        with open(result_path, "r", encoding="utf-8") as file:
            # 使用正则表达式提取 "-" 和 ".txt" 之间的字符
            data["链接"] = re.search(r'-(.*?)\.txt', file_name).group(1) if re.search(r'-(.*?)\.txt', file_name) else ''
            lines = file.readlines()
            data["标题"] = lines[0].strip()

        for i, line in enumerate(lines):
            # 查找】和\n的位置
            end_bracket_index = line.find("】")
            newline_index = line.find("\n")
            if "【发布部门】" in line:
                data["发布部门"] = get_data(line)
            if "【批准部门】" in line:
                data["批准部门"] = get_data(line)
            if "【发文字号】" in line:
                data["发文字号"] = get_data(line)
            if "【批准日期】" in line:
                data["批准日期"] = get_data(line)
            if "【发布日期】" in line:
                data["日期"] = get_data(line).split(".")[0]
            if "【时效性】" in line:
                data["时效性"] = get_data(line)
            if "【失效依据】" in line:
                data["失效依据"] = get_data(line)
            if "【效力级别】" in line:
                data["效力级别"] = get_data(line)
            if "【法规类别】" in line:
                data["法规类别"] = get_data(line)
            if "【关键词】" in line:
                data["关键词"] = get_data(line)
            if "【专题分类】" in line:
                data["专题分类"] = get_data(line)
        # 添加文件路径和文件夹名称
        data["文件夹名称"] = ""
        extracted_data.append(data)

# 将数据保存为CSV文件
data = pd.DataFrame(extracted_data)

# 检查文件是否存在
result_path = "result/data.xlsx"
if os.path.exists(result_path):
    # 如果文件存在，删除它
    os.remove(result_path)
# 保存数据
data.to_excel(result_path, index=False, encoding="utf-8")
print("数据提取完成!")
sys.exit(0)
