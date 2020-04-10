import json
# 测试解析文件
with open('data.txt', "r") as f:  # 打开文件
    data = f.read()  # 读取文件
    print(data)
    # json_str = resp.json(data)
    reslult = json.loads(data)
    total = reslult['total']
    pages = total // 100
    if total % 100 > 0:
        pages += 1

    for i in range(pages):
        if i == 0:
            continue
        print(i)
    print(reslult['total'])
    data_list = reslult['data']
    for i in data_list:
        print(i)
