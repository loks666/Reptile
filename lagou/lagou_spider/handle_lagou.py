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
        self.header = {'Access-Control-Allow-Credentials': 'true',
                       'Access-Control-Allow-Headers': 'authorization,X-L-REQ-HEADER,Content-Type,X-Anit-Forge-Token,X-Anit-Forge-Code,SHOP-ORDER-TOKEN,X-Requested-With,coop51-ctmid,coop51-hruid,coop51-accesskey,Coop51-InnerToken, edu-referer,X-K-HEADER,X-S-HEADER,X-SS-REQ-HEADER,X-Anit-Verify-Info',
                       'Access-Control-Allow-Methods': 'POST, GET, PUT, PATCH, DELETE',
                       'Access-Control-Allow-Origin': 'https://www.lagou.com',
                       'Access-Control-Expose-Headers': 'Pard-Id,Coop51-InnerToken,X-S-HEADER,X-SS-REQ-HEADER',
                       'Connection': 'keep-alive',
                       'Content-Type': 'application/json;charset=UTF-8',
                       'Date': 'Sat, 30 Apr 2022 14:43:01 GMT',
                       'Pard-Id': '30436.23895.16513297811400089',
                       'Pard-Id': '30436.23895.16513297811400089',
                       'Server': 'GatW',
                       'Transfer-Encoding': 'chunked',
                       'Vary': 'Accept-Encoding',
                       'X-Application-Context': 'lg-zuul-boot-v1:pro-c:12760',
                       'X-L-STATE': '1',
                       'X-S-HEADER': 'Qr8z+Ncbb5rMVO1XmUCjx4m2VVrJFVW4tPygfbLjJ6TxZwhLJxnHKRWgSjcBp96qI65YPfWcc3GWxjJdmIjbAaamFiyqAmVWMNH2gkYcqVxXo6waNP1fy2skhufbK0FhM0PvCI0hy/kg83szEIo+Lmvufk8PA6jkFn7lo0FctVwjtX6LDvJpmrWebnXXNu/U',
                       'accept': 'application/json, text/javascript, */*; q=0.01',
                       'Accept-Encoding': 'gzip, deflate, br',
                       'Accept-Language': 'zh-CN,zh;q=0.9,ru;q=0.8',
                       'Connection': 'keep-alive',
                       'Cookie': '_ga=GA1.2.1138158517.1651327863; _gid=GA1.2.987242203.1651327863; user_trace_token=20220430221105-7ab16d23-1d0a-43f3-a6f2-4e715db13b6f; LGUID=20220430221105-6c7c2436-cfbb-48e3-8274-4a77499b0aa2; sajssdk_2015_cross_new_user=1; sensorsdata2015session=%7B%7D; LGSID=20220430221105-770cf8f3-c647-47be-a954-8cc380d71bb4; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1651327863; __lg_stoken__=4b20d941cbb295574f7ce9387e5a3b1f616fd6d908aab8ab34a5d4543a3b6bc5e3cea67f52223e71de77c3eb9b908f1bcde6144c125d06af4aa41f6e5abd7e11beca905511ed; gate_login_token=99809822a05295aa7a388ac8ea22b41f7f87038221338a1c; LG_LOGIN_USER_ID=09729e69a2528547363010c7b61d0ece79e81f70ab06c32f; LG_HAS_LOGIN=1; _putrc=08CF68A7A735732F; login=true; unick=%E6%9D%8E%E7%BF%94; index_location_city=%E4%B8%8A%E6%B5%B7; __SAFETY_CLOSE_TIME__6007201=1; privacyPolicyPopup=false; _gat=1; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1651329772; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%226007201%22%2C%22first_id%22%3A%221807acf887717-0cba4829d54e62-9771a39-2073600-1807acf8878e0f%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2299.0.4844.84%22%2C%22lagou_company_id%22%3A%22%22%7D%2C%22%24device_id%22%3A%221807acf887717-0cba4829d54e62-9771a39-2073600-1807acf8878e0f%22%7D; X_HTTP_TOKEN=e99bcc6d139b97740879231561d4dc3ba9167ebddf; LGRID=20220430224301-7a725b05-4f56-4e5d-9034-b1af2b6f0034',
                       'Host': 'gate.lagou.com',
                       'Origin': 'https://www.lagou.com',
                       'Referer': 'https://www.lagou.com/',
                       'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
                       'sec-ch-ua-mobile': '?0',
                       'sec-ch-ua-platform': '"Windows"',
                       'Sec-Fetch-Dest': 'empty',
                       'Sec-Fetch-Mode': 'cors',
                       'Sec-Fetch-Site': 'same-site',
                       'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
                       'X-K-HEADER': 'QQJn07JSX/CYKNWw02E5IA+KedBGvBD8fhv/Ii6yoqQqNhgnr9h2teUHAwDyhG05',
                       'x-l-req-header': '{deviceType:1}',
                       'X-S-HEADER': '4UlydsVaIep69lS53LO2G04juoKxSvGPaOLnliJ0UP5nD9wYAssLKnCrPiL/OxR4Nu6Oj2Cf7pzPAMzjxHAqrxsbRuTVOeUgXyXYXnFpBjQ/9k7YSUTGcOS6mIhbgAwE1HsHU8L0DU8I6MUyFF4snA==',
                       'X-SS-REQ-HEADER': '{"secret":"QQJn07JSX/CYKNWw02E5IA+KedBGvBD8fhv/Ii6yoqQqNhgnr9h2teUHAwDyhG05"}'}
        # self.header = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
        #                   'Chrome/81.0.4044.129 Safari/537.36'}
        self.city_list = ''

    # 获取全国所有城市
    def handle_city(self):
        f = open("citys.json", "r", encoding='utf-8')
        data = json.loads(f.read())
        city_list = data['city']
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
        proxyinfo = "https://%s:%s@%s:%s" % ('H9N137501G5053ZD', '2CBABB5D337D3A37', 'http-dyn.abuyun.com', '9020')
        proxy = {
            "http": proxyinfo,
            "https": proxyinfo
        }
        while True:
            try:
                if method == 'get':
                    response = self.lagou_session.get(url=url, headers=self.header, verify=False, proxies=proxy,
                                                      timeout=6)
                    response.encoding = 'utf-8'
                elif method == 'post':
                    response = self.lagou_session.post(url=url, headers=self.header, data=data, verify=proxy,
                                                       proxies=None, timeout=6)
            except Exception as e:
                print(e)
                # 清除cookies信息
                self.lagou_session.cookies.clear()
                # 重新获取cookies信息
                self.handle_request("get", get_url % info)
                # time.sleep(10)
            response.encoding = 'utf-8'
            if '频繁' in response.text:
                print(response.text)
                # 清除cookies信息
                self.lagou_session.cookies.clear()
                # 重新获取cookies信息
                self.handle_request("get", get_url % info)
                # time.sleep(10)
                continue
            return response.text


if __name__ == '__main__':
    lagou = HandleLaGou()
    print(lagou.handle_city())
    # 引入多进程加速抓取
    lagou.city_job(city='上海')
    # pool = multiprocessing.Pool(3)
    # for city in lagou.city_list:
    #     print('进来了')
    #     pool.apply_async(lagou.city_job, args=('shanghai',))
    # pool.close()
    # pool.join()
