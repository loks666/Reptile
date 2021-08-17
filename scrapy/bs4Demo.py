import re
import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.cnblogs.com')
soup = BeautifulSoup(r.text, 'lxml')  # lxml为解析器

print(soup.title, soup.title.string)  # 获取指定标签，获取指定标签里面的内容
print(soup('title'), soup('title')[0].string)  # 获取指定标签也可以写成这样
print(soup.meta.get('charset'))  # 获取指定标签的属性
print(soup.meta['charset'])  # 获取指定标签的属性也可写成这样
print(soup.meta)  # 获取第一个标签（多个只取第一个）
print(soup.find('meta'))  # 获取第一个标签，结果和上面一样
print(soup.find('meta', attrs={'name': 'viewport'}))  # 获取第一个标签，根据属性过滤获取
print(soup.find_all('meta', attrs={'charset': True}))  # 获取所有标签的列表，同时根据是否含有属性charset过滤获取
