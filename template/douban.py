# -*- coding: utf-8 -*-
# author:Gary
import html
import json
from xml import etree

import requests  # 获取网页内容
from bs4 import BeautifulSoup  # 解析网页内容
import re  # 正则匹配内容


# 获取网页的内容
def get_html(urls, proxy):
    print(proxy)
    try:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/79.0.3945.130 Safari/537.36'}
        proxyHost = proxy['ip']
        proxyPort = proxy['port']
        proxyMeta = "http://%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
        }
        proxies = {
            "http": proxyMeta,
            "https": proxyMeta
        }
        res = requests.get(urls, headers=header, proxies=proxies)
        print(res.status_code)
        if res.status_code == 403:
            get_html(urls, get_proxy())
        res.encoding = 'utf-8'
        return res.text  # 返回网页的内容
    except RuntimeError:
        return None


# 通过bs4解析，主要是标签选择器
def ana_by_bs4(html):
    soup = BeautifulSoup(html, 'html.parser')  # 注意需要添加html.parser解析
    lis = soup.select("ol li")  # 选择ol li标签
    for li in lis:
        index = li.find('em').text  # 索引
        title = li.find_all('span', class_='title')  # 正标题
        the_title = title[0].text  # 正标题
        if len(title) > 1:  # 如果title存在两个则表明存在副标题
            sub_title = title[1].text
        else:
            sub_title = ''
        try:
            other_title = li.find('span', class_='other').text  # 其他标题
        except:
            other_title = ''
        actor = li.find('div', class_='bd').find('p').text.split('\n')[1].strip()  # 导演和演员
        strInfo = re.search("(?<=<br/>).*?(?=<)", str(li.select_one(".bd p")), re.S | re.M).group().strip()  # 年份、国家、类型
        infos = strInfo.split('/')
        year = infos[0].strip()  # 年份
        area = infos[1].strip()  # 国家，地区
        m_type = infos[2].strip()  # 类型
        rating = li.find('span', class_='rating_num').text  # 评分
        remark_num = li.find('div', class_='star').find_all('span')[3].text[:-3]  # 评分人数
        try:
            quote = li.find('span', class_='inq').text  # 名言
        except NameError:  # 名言可能不存在
            quote = ''
        # print(actor)
        print(index, the_title, sub_title, other_title, actor, year, area, m_type, rating, remark_num, quote)


def get_proxy():
    url = 'http://tiqu.pyhttp.taolop.com/getip?count=1&neek=15925&type=2&yys=0&port=2&sb=&mr=2&sep=0&ts=1&ys=1&cs=1'
    response = requests.get(url)
    if response.status_code == 200:
        str = json.loads(response.text)
        ip_list = str['data']
        print(response.text)
        return ip_list[0]
    else:
        print('failed')


if __name__ == '__main__':
    url = 'https://www.douban.com/group/search?cat=1019&q={}'.format('上海')
    htmldoc = get_html(urls=url, proxy=get_proxy())

    soup = BeautifulSoup(htmldoc, "html.parser")
    result = soup.find_all(attrs={'class': 'result'})
    for item in result:
        print(item.text)

    # print(result.text)
    # selector = html.etree.HTML(htmldoc)
    # print(selector.xpath('//div[@class="result"]'))
