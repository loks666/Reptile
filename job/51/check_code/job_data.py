import time

import requests
from bs4 import BeautifulSoup


class Job(object):
    global get_url
    global positionType
    positionType = 'java'
    # get_url = 'https://search.51job.com/'
    get_url = 'https://search.51job.com/list/020000,000000,0000,00,9,99,java,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='

    def __init__(self):
        # 使用session保存cookie信息
        self.session = requests.session()
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}

    def job_list(self):
        html = self.request(method="get", url=get_url)
        soup = BeautifulSoup(html, "html.parser")

        print(soup.find_all('span',attrs = 'td'))

    def request(self, method, url, data=None, info=None):
        # 加入动态代理
        proxyinfo = "http://%s:%s@%s:%s" % ('H9N137501G5053ZD', '2CBABB5D337D3A37', 'http-dyn.abuyun.com', '9020')
        proxy = {
            "http": proxyinfo,
            "https": proxyinfo
        }
        # 消除ssl警告
        requests.packages.urllib3.disable_warnings()
        while True:
            try:
                if method == 'get':
                    response = self.session.get(url=url, headers=self.header, verify=False, proxies=None,
                                                timeout=6)
                    response.encoding = 'utf-8'
                elif method == 'post':
                    response = self.session.post(url=url, headers=self.header, data=data, verify=False,
                                                 proxies=None, timeout=6)
            except:
                # 清除cookies信息
                self.session.cookies.clear()
                # 重新获取cookies信息
                self.request("get", get_url % info)
                time.sleep(10)
            response.encoding = 'gbk'
            return response.text


if __name__ == '__main__':
    job51 = Job()
    job51.job_list()