import json
import requests
import multiprocessing
# from lagou_spider.handle_insert_data import lagou_mysql
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import time
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from lagou.lagou_spider.handle_insert_data import lagou_mysql

s = Service(executable_path=r'H:\Project\Python\Reptile\51job\chromedriver.exe')
browser = webdriver.Chrome(service=s)
browser.set_window_position(3841, 0)
browser.maximize_window()
wait = WebDriverWait(browser, 10)


class HandleLaGou(object):
    def __init__(self):
        # 使用session保存cookies信息
        self.lagou_session = browser.get_cookies()
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        # 读取json文件内容,返回字典格式
        with open('citys.json', 'r', encoding='utf8') as fp1:
            json_data = json.load(fp1)
        self.city_list = set(json_data['city'])
        # self.lagou_session.cookies.clear()
        # handle_city()

    def handle_city_job(self, city):
        first_request_url = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=true&labelWords=&suginput=" % city
        browser.get(first_request_url)
        first_response = browser.page_source
        # first_response = self.handle_request(method="GET", url=first_request_url)
        total_page_search = re.compile(r'class="span\stotalNum">(\d+)</span>')
        try:
            total_page = total_page_search.search(first_response).group(1)
            print(city, total_page)
        # 由于没有岗位信息造成的exception
        except Exception as e:
            return e
        else:
            for i in range(1, int(total_page) + 1):
                data = {
                    "pn": i,
                    "kd": "python"
                }
                page_url = "https://www.lagou.com/jobs/positionAjax.json?city=%s&needAddtionalResult=false" % city
                referer_url = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=true&labelWords=&suginput=" % city
                # referer的URL需要进行encode
                # self.header['Referer'] = referer_url.encode()
                browser.get(first_request_url)
                response = browser.page_source
                # response = self.handle_request(method="POST", url=page_url, data=data, info=city)
                lagou_data = json.loads(response.text())
                job_list = lagou_data['content']['positionResult']['result']
                for job in job_list:
                    lagou_mysql.insert_item(job)

    def handle_request(self, method, url, data=None, info=None):
        while True:
            # 加入阿布云的动态代理
            proxyinfo = "http://%s:%s@%s:%s" % (
                '864839856801861632', 'cTQvA3Ib', 'http-short.xiaoxiangdaili.com', '10010')
            proxy = {
                "http": proxyinfo,
                "https": proxyinfo
            }
            try:
                if method == "GET":
                    response = self.lagou_session.get(url=url, headers=self.header, proxies=proxy, timeout=6)
                    # response = self.lagou_session.get(url=url,headers=self.header,timeout=6)
                elif method == "POST":
                    response = self.lagou_session.post(url=url, headers=self.header, data=data, proxies=proxy,
                                                       timeout=6)
                    # response = self.lagou_session.post(url=url,headers=self.header,data=data,timeout=6)
            except:
                # 需要先清除cookies信息
                self.lagou_session.cookies.clear()
                # 重新获取cookies信息
                first_request_url = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=true&labelWords=&suginput=" % info
                self.handle_request(method="GET", url=first_request_url)
                time.sleep(10)
                continue
            response.encoding = 'utf-8'
            if '频繁' in response.text:
                print(response.text)
                # 需要先清除cookies信息
                self.lagou_session.cookies.clear()
                # 重新获取cookies信息
                first_request_url = "https://www.lagou.com/jobs/list_python?city=%s&cl=false&fromSearch=true&labelWords=&suginput=" % info
                self.handle_request(method="GET", url=first_request_url)
                time.sleep(10)
                continue
            return response.text


# 点击
def click(selector):
    button = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
    button.click()


# css文本输入
def input_keys(selector, keys):
    inputs = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
    inputs.clear()
    inputs.send_keys(keys)


def login():
    browser.get('https://www.lagou.com/')
    browser.refresh()
    click('/html/body/div[10]/div[1]/div[2]/div[2]/button[4]')
    click('//*[@id="lg_tbar"]/div[1]/div[2]/ul/li[1]/a')
    input("登陆完成按回车")


if __name__ == '__main__':
    login()
    lagou = HandleLaGou()
    for city in lagou.city_list:
        lagou.handle_city_job(city)
