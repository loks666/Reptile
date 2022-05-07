import json
from datetime import datetime

import shutil
import numpy as np
from PIL import Image
import os
import datetime

nowTime = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


def remove_file(old_path, new_path):
    files = os.listdir(old_path)
    print(files)
    for file in files:
        old = os.path.join(old_path, file)
        new = os.path.join(new_path, file)
        shutil.move(old, new)


def save_json():
    dictObj = {
        'data': [1, 2, 3, 4, 5]
    }
    jsObj = json.dumps(dictObj)
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = 'test_' + now + '.json'
    fileObject = open(filename, 'w')
    fileObject.write(jsObj)
    fileObject.close()


def compare_size(size1, size2):
    with open(size1, "rb") as f1:
        size1 = len(f1.read())
    with open(size2, "rb") as f2:
        size2 = len(f2.read())
    if size1 == size2:
        return "size_same"
    else:
        return "size_different"


def compare_length(length1, length2):
    length1 = Image.open(length1)
    length2 = Image.open(length2)
    if length1.size == length2.size:
        return "length_same"
    else:
        return "length_different"


def compare_content(content1, content2):
    content1 = np.array(Image.open(content1))
    image2 = np.array(Image.open(content2))
    if np.array_equal(content1, image2):
        return "content_same"
    else:
        return "content_different"


def is_same(same1, same2):
    # 比较两张图片是否same
    # 第一步：比较size_是否same
    # 第二步：比较长和宽是否same
    # 第三步：比较每个像素是否same
    # 如果前一步不same，则两张图片必不same
    size = compare_size(same1, same2)
    if size == "size_same":
        length = compare_length(same1, same2)
        if length == "length_same":
            content = compare_content(same1, same2)
            if content == "content_same":
                return "two images is different"


def distinct():
    os.makedirs(save_path, exist_ok=True)

    # 获取图片列表 file_map，字典{文件路径filename : 文件size_image_size}
    file_map = {}
    image_size = 0
    # 遍历filePath下的文件、文件夹（包括子目录）
    for parent, dir_names, filenames in os.walk(load_path):
        # for dirname in dirname:
        # print('parent is %s, dirname is %s' % (parent, dirname))
        for filename in filenames:
            print(filename)
            # print('parent is %s, filename is %s' % (parent, filename))
            # print('the full name of the file is %s' % os.path.join(parent, filename))
            image_size = os.path.getsize(os.path.join(parent, filename))
            file_map.setdefault(os.path.join(parent, filename), image_size)

    # 获取的图片列表按 文件size_image_size 排序
    file_map = sorted(file_map.items(), key=lambda d: d[1], reverse=False)
    file_list = []
    for filename, image_size in file_map:
        file_list.append(filename)

    # 取出重复的图片
    file_repeat = []
    for currIndex, filename in enumerate(file_list):
        image1 = file_list[currIndex]
        if ~image1.endswith('.jpg'):
            future = os.path.join(save_path, os.path.basename(image1))
            face_id = 1
            if os.path.exists(future):
                old_name = os.path.basename(image1)
                name_list = old_name.split('.')
                prefix = name_list[0]
                suffix = name_list[1]
                temp = prefix + '(%s).' + suffix
                rename = temp % face_id
                print(rename)
                future = os.path.join(save_path, rename)
                while os.path.exists(future):
                    face_id += 1
                    temp = prefix + '(%s).' + suffix
                    rename = temp % face_id
                    future = os.path.join(save_path, rename)
                print(future)
                result = os.path.join(os.path.dirname(image1), os.path.basename(future))
                print(result)
                os.rename(image1, result)
                image1 = result
            shutil.move(image1, save_path)
            continue
        dir_image2 = file_list[currIndex + 1]
        result = is_same(image1, dir_image2)
        if result == "two images is different":
            file_repeat.append(file_list[currIndex + 1])
            print("same image：", file_list[currIndex], file_list[currIndex + 1])
        else:
            print('different image：', file_list[currIndex], file_list[currIndex + 1])
        currIndex += 1
        if currIndex >= len(file_list) - 1:
            break

    # 将重复的图片移动到新的文件夹，实现对原文件夹降重
    for image in file_repeat:
        shutil.move(image, save_path)
        print("正在移除重复照片：", image)


if __name__ == '__main__':
    # load_path = 'E:\\1'  # 要去重的文件夹
    load_path = 'E:\\remove'  # 要去重的文件夹
    # save_path = 'E:\\2'  # 空文件夹，用于存储检测到的重复的照片
    save_path = 'E:\\total'  # 空文件夹，用于存储检测到的重复的照片
    distinct()
    # print(is_same('E:\\total\\2.jpg', 'E:\\total\\3.jpg'))
