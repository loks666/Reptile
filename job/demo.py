import re
import time

from bs4 import  BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from pyquery import pyquery
from selenium.webdriver.support.wait import WebDriverWait
import os

chromedriver = "chromedriver.exe"
os.environ["webdriver.Chrome.driver"] = chromedriver

browser = webdriver.Chrome(chromedriver)
browser.maximize_window()

url = 'http://biz.smpaa.cn/ysxtqxcp/login.jsp'
wait = WebDriverWait(browser, 10)


def login():
    browser.get(url)
    input_keys('//*[@id="loginName"]', 'zk1509005!')
    input_keys('//*[@id="password"]', '18412914!')
    click('//*[@id="captcha"]')
    time.sleep(1)
    click('/html/body/div[2]/div[2]/div[2]/div/div[1]')

    browser.refresh()
    # 点击企业
    click('//*[@id="mainSplitter"]/div/div[1]/div/div/div/ul/li/a')
    # 信息查询
    click('//*[@id="mini-3$3"]/div[1]/div[2]')
    # 采购单信息查询
    click('//*[@id="10202004$text"]')

    # browser.find_element_by_xpath('//*[@id="mini-27"]/div[1]/table/tbody/tr/td[1]/span[3]/input')
    # 查询
    time.sleep(1)

def get_data():
    html = browser.page_source
    with open('test.text', 'w') as f:
        f.write(html)
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('div', class_="mini-toolbar")
    print(table)
    # print(html)
    # items = doc('#dgCgdxx > div > div.mini-panel-viewport.mini-grid-viewport > div.mini-panel-body.mini-grid-rows > div.mini-grid-rows-view > div > table > tbody').items()
    # for item in items:
    #     print(item)


def next_page():
    try:
        # 点击下一页
        click('//*[@id="mini-33"]')
    except TimeoutException:
        next_page()


# css文本输入
def input_keys(selector, keys):
    input = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
    input.clear()
    input.send_keys(keys)


# 点击
def click(selector):
    button = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
    button.click()



def main():
    login()
    get_data()
    # search()
    # page_size = int(search())
    # for i in range(2, page_size + 1):
    #     next_page(i)



if __name__ == '__main__':
    main()
