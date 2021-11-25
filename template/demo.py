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
                      'Chrome/95.0.4638.69 Safari/537.36',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://movie.douban.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    proxies = {'http': None, 'https': None}
    res = requests.get(target_url, headers=header)
    # 获取网页，并带有伪装的浏览器头，一般好的网站会有检测是不是程序访问
    res.encoding = res.apparent_encoding  # 设置编码，防止乱码
    # print(res.text)#输出网页内容
    return etree.HTML(res.content)


# 通过bs4解析，主要是标签选择器
def get_by_bs4(html):
    pass


def save():
    filename = 'test.html'
    with open(filename, 'w') as file_object:
        file_object.write(str(html).encode('utf-8'))


if __name__ == '__main__':
    target = 'https://www.douban.com/group/search?cat={}&q={}'.format(1019, '上海');
    html = get_html(target)
    print(html.text)
    result = html.xpath('//div[@class="content"]/text()')
    print()
    print(result)
