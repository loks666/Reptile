# -*- coding: utf-8 -*-
# author:Gary
import json

import requests  # 获取网页内容
from bs4 import BeautifulSoup  # 解析网页内容
import re  # 正则匹配内容


# 获取网页的内容
def get_html(urls):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/79.0.3945.130 Safari/537.36'}
    proxyHost = "ip"
    proxyPort = "port"
    proxyMeta = "http://%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
    }
    proxies = {
        "http": proxyMeta,
        "https": proxyMeta
    }
    res = requests.get(urls, headers=header)  # 获取网页，并带有伪装的浏览器头，一般好的网站会有检测是不是程序访问
    res.encoding = res.apparent_encoding  # 设置编码，防止乱码
    # print(res.text)#输出网页内容
    return res.text  # 返回网页的内容


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
    url = 'http://tiqu.pyhttp.taolop.com/getflowip?count=1&neek=15925&type=2&sep=4&sb=&ip_si=1&mr=0'
    restponse = requests.get(url)
    if restponse.status_code == 200:
        print()
    else:
        print()


if __name__ == '__main__':
    # get_proxy()
    str = '{"code":0,"data":[{"ip":"140.249.72.22","outip":"182.38.207.135","port":35150},{"ip":"140.249.72.43","outip":"113.94.59.162","port":26408},{"ip":"140.249.72.43","outip":"114.239.89.154","port":21333}],"msg":"0","success":true}'

    user_dic = json.loads(str)
    print(user_dic['data'])
    for page in range(10):
        # url = 'https://www.douban.com/group/search?cat=1019&q={}'.format('上海')
        url = 'https://www.douban.com'
        # proxy_url = 'http://tiqu.pyhttp.taolop.com/getflowip?count=5&neek=15925&type=2&sep=4&sb=&ip_si=1&mr=0'
        # proxys = get_proxy(proxy_url)
        # print(proxys)
        # text = get_html(url)  # 获取网页内容
        # print(text)
        # soup = BeautifulSoup("<html>A Html Text</html>", "html.parser")
        # ana_by_bs4(text)  # bs4方式解析
