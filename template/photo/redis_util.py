import redis

rds = redis.Redis(host='localhost', port=6379, decode_responses=True)
rds.set('name', 'runoob')  # 设置 name 对应的值
print(rds['name'])
print(rds.get('name'))  # 取出键 name 对应的值
print(type(rds.get('name')))  # 查看类型
