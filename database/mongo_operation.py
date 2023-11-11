import os
import sys

from my_mongoengine import MongoDBHandler

# 替换为你的文件夹路径、数据库名称和集合名称
folder_path = r'D:\Users\Documents\预设'
database_name = 'jax'
collection_name = 'file'

mongo_handler = MongoDBHandler(database_name, collection_name)


def save_files_to_mongo(path):
    # 实例化 MongoDBHandler 类

    for root, dirs, files in os.walk(path):
        for file in files:
            print(file)
            # 获取文件路径
            file_path = os.path.join(root, file)

            # 获取文件名和文件类型
            file_name, file_extension = os.path.splitext(file)
            file_extension = file_extension.lower().replace(".", "")

            # 将数据保存到 MongoDB
            mongo_handler.insert_data(file_path, file_name, file_extension)


if __name__ == '__main__':
    save_files_to_mongo(folder_path)
    # 查询文件类型为空字符串的数据
    query = {"文件类型": ""}
    result = mongo_handler.query_data(query)
    for document in result:
        print(document)
    # 退出程序
    sys.exit()
