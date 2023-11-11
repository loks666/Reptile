# my_mongoengine.py

from mongoengine import connect, Document, StringField


class MongoDBHandler:
    def __init__(self, database_name, collection_name):
        self.connect_to_mongo(database_name)
        self.collection = self.create_collection(collection_name)

    def connect_to_mongo(self, database_name):
        # 连接到 MongoDB
        connect(database_name, host='localhost', port=27017)

    def create_collection(self, collection_name):
        # 创建集合
        class MyDocument(Document):
            文件路径 = StringField(required=True)
            文件名 = StringField(required=True)
            文件类型 = StringField(required=True)
            meta = {
                'collection': collection_name  # 替换为你想要的集合名称
            }

        return MyDocument

    def insert_data(self, file_path, file_name, file_type):
        # 插入数据到 MongoDB
        document = self.collection(文件路径=file_path, 文件名=file_name, 文件类型=file_type)
        document.save()

    def update_data(self, query, new_data):
        # 更新数据
        self.collection.objects(**query).update_one(**new_data)

    def query_data(self, query):
        # 查询数据
        return self.collection.objects(**query)

    def delete_data(self, query):
        # 删除数据
        self.collection.objects(**query).delete()
