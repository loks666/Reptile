import json
import multiprocessing
import time

import requests
from lxml import etree
import urllib3
from urllib3.exceptions import InsecureRequestWarning

from lagou.lagou_spider.handle_insert_data import lagou_mysql

urllib3.disable_warnings(InsecureRequestWarning)


class HandleLaGou(object):
    global get_url
    global positionType
    positionType = 'java'
    get_url = 'https://www.lagou.com/jobs/list_java?&px=default&city=%s'

    def __init__(self):
        # 使用session保存cookie信息
        self.lagou_session = requests.session()
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
        self.city_list = ''

    # 获取全国所有城市
    def handle_city(self):
        city_url = 'https://www.lagou.com/jobs/allCity.html'
        city_html = self.handle_request(method="get", url=city_url)
        selector = etree.HTML(city_html)
        # xpath获取城市列表
        city_list = selector.xpath('//ul[@class="city_list"]//a/text()')
        print(city_list)
        self.city_list = city_list
        self.lagou_session.cookies.clear()

    def city_job(self, city):

        get_response = self.handle_request("get", get_url % city)
        total_num = etree.HTML(get_response).xpath('//span[@class="span totalNum"]/text()')
        total_num = total_num[0]
        for i in range(1, int(total_num) + 1):
            data = {
                'pn': i,
                'kd': positionType
            }
            page_url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&city=%s&needAddtionalResult=false' % city
            referer = get_url % city
            self.header['Referer'] = referer.encode()
            post_response = self.handle_request('post', url=page_url, data=data, info=city)
            print(post_response)
            lagou_data = json.loads(post_response)
            job_list = lagou_data['content']['positionResult']['result']
            for job in job_list:
                lagou_mysql.insert_item(job)

    def handle_request(self, method, url, data=None, info=None):
        # 加入动态代理
        proxyinfo = "http://%s:%s@%s:%s" % ('H9N137501G5053ZD', '2CBABB5D337D3A37', 'http-dyn.abuyun.com', '9020')
        proxy = {
            "http": proxyinfo,
            "https": proxyinfo
        }
        while True:
            try:
                if method == 'get':
                    response = self.lagou_session.get(url=url, headers=self.header, verify=False, proxies=None,
                                                      timeout=6)
                    response.encoding = 'utf-8'
                elif method == 'post':
                    response = self.lagou_session.post(url=url, headers=self.header, data=data, verify=False,
                                                       proxies=None, timeout=6)
            except:
                # 清除cookies信息
                self.lagou_session.cookies.clear()
                # 重新获取cookies信息
                self.handle_request("get", get_url % info)
                time.sleep(10)
            response.encoding = 'utf-8'
            if '频繁' in response.text:
                print(response.text)
                # 清除cookies信息
                self.lagou_session.cookies.clear()
                # 重新获取cookies信息
                self.handle_request("get", get_url % info)
                time.sleep(10)
                continue
            return response.text


if __name__ == '__main__':
    lagou = HandleLaGou()
    lagou.handle_city()
    # 引入多进程加速抓取
    pool = multiprocessing.Pool(3)
    for city in lagou.city_list:
        pool.apply_async(lagou.city_job, args=(city,))
    pool.close()
    pool.join()
