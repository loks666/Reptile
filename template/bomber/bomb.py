import time

import requests
from bs4 import BeautifulSoup


class Job(object):
    global positionType
    positionType = 'java'

    # get_url = 'https://search.51job.com/'

    def __init__(self):
        # 使用session保存cookie信息
        self.session = requests.session()
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}

    def job_list(self, url):
        html = self.request(method="get", url=url)
        soup = BeautifulSoup(html, "html.parser")

        print(soup.find_all('span', attrs='td'))

    def request(self, method, url, data, info=None):
        # 加入动态代理
        global response
        proxyinfo = "http://%s:%s@%s:%s" % ('H9N137501G5053ZD', '2CBABB5D337D3A37', 'http-dyn.abuyun.com', '9020')
        proxy = {
            "http": proxyinfo,
            "https": proxyinfo
        }
        # 消除ssl警告
        requests.packages.urllib3.disable_warnings()
        try:
            if method == 'get':
                response = self.session.get(url=url, headers=self.header, verify=False, proxies=None,
                                            timeout=6)
                response.encoding = 'utf-8'
            elif method == 'post':
                response = self.session.post(url=url, headers=self.header, data=data, verify=False,
                                             proxies=None, timeout=6)
            # response.encoding = 'gbk'
        except RuntimeError:
            # 清除cookies信息
            self.session.cookies.clear()
            # 重新获取cookies信息
            self.request("get", url % info)
            time.sleep(10)
        return response.text


if __name__ == '__main__':
    job51 = Job()
    url = 'http://test.marketing.i.vipcode.com/api/marketing/dataStatistics/sendCode'
    data = {'phone': '16621370084'}
    method = 'POST'
    response = requests.post(url, data)
    print(response.text)
    # print(job51.request(method, url, data))
