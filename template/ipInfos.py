'''
爬取国内高匿代理IP
author: Python当打之年
'''
import random
import time

import requests
from bs4 import BeautifulSoup


def get_ipinfo(url, headers):
    ipinfo = []
    # 爬取前50页代理
    for i in range(1, 50):
        try:
            url0 = url.format(i)
            # 随机延时，避免请求频率过快导致网络瘫痪
            time.sleep(random.uniform(3.1, 4.2))
            # 发送网页请求
            html = requests.get(url0, headers=headers, timeout=10)
            soup = BeautifulSoup(html.text, 'lxml')
            # 分析IP列表
            tr_list = soup.select_one('.fl-table').select_one('tbody').select('tr')
            # 遍历每一行，获取IP
            for td_list in tr_list:
                # 过滤，仅获取高匿、有效期超过1天的IP
                if '高匿' in td_list.select('td')[2].text and '天' in td_list.select('td')[5].text:
                    ipport = td_list.select('td')[0].text
                    ipinfo.append(ipport)
        except IOError:
            continue
            # 返回满足要求IP
            return ipinfo


def check_ip(ippost_info, headers):
    # http://icanhazip.com IP测试网址
    check_url = 'http://icanhazip.com'
    proxies = {'http': 'http://' + ippost_info, 'https': 'https://' + ippost_info}
    try:
        time.sleep(1)
        # 发送测试请求
        r = requests.get(check_url, headers=headers, proxies=proxies, timeout=10)
        if r.status_code == 200:
            print('有效IP：' + ippost_info)
            with open('xila_https_list.txt', 'a') as f:
                f.write(ippost_info)
                f.write('\n')
        else:
            print('无效IP：' + ippost_info)
    except IOError:
        print('无效IP：' + ippost_info)


if __name__ == '__main__':
    url = "http://www.xiladaili.com/http/"
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/81.0.4044.129 Safari/537.36'}
    get_ipinfo(url, header)
