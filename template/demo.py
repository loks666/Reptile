# -*- coding: utf-8 -*-
# author:Gary
import requests  # 获取网页内容
from bs4 import BeautifulSoup  # 解析网页内容
import re  # 正则匹配内容

# 获取网页的内容
from lxml import etree


def get_html(target_url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/96.0.4664.45 Safari/537.36',
        'Cookie': ''}

    proxies = {"http": None, "https": None}
    res = requests.get(target_url, headers=header, proxies=proxies)
    # 获取网页，并带有伪装的浏览器头，一般好的网站会有检测是不是程序访问
    res.encoding = res.apparent_encoding  # 设置编码，防止乱码
    # print(res.text)#输出网页内容
    return etree.parse(res.content)  # 返回网页的内容


# 通过bs4解析，主要是标签选择器
def get_by_bs4(html):
    pass


def save():
    filename = 'test.html'
    with open(filename, 'w') as file_object:
        file_object.write(str(html).encode('utf-8'))


if __name__ == '__main__':
    target = "https://www.douban.com/group/search?cat={}&q={}".format(1019, '上海');
    html = get_html(target)
    result = html.xpath("")
    print('\n')
    print(result)
    html = BeautifulSoup(html, 'lxml')

    attrs_place = html.xpath(attrs={"id": "places_neighbours__row"})
    # print(attrs_place)
    pd.read_csv('D:/test/t1.csv').to_parquet
