import re
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import os

chromedriver = "你的路径地址\chromedriver.exe"
os.environ["webdriver.Chrome.driver"] = chromedriver
browser = webdriver.Chrome(chromedriver)
browser.maximize_window()

url = 'https://login.51job.com/'
wait = WebDriverWait(browser, 10)


def login():
    browser.get(url)
    input_keys('#loginname', '你的账号')
    input_keys('#password', '你的密码')
    click('#login_btn')


def search():
    try:
        # 点击首页
        click('#topIndex > div > p > a:nth-child(1)')
        # 搜索职位
        input_keys('#kwdselectid', '你要投递的职位')
        click('body > div.content > div > div.fltr.radius_5 > div > button')
        # 获取页数
        page = browser.find_element_by_css_selector(
            '#resultList > div.dw_page > div > div > div > span:nth-child(3)').text
        return re.findall("\d+", page)[0]
    except TimeoutException:
        return search()


def next_page(page_num):
    try:
        # 全选
        click('#top_select_all_jobs_checkbox')
        # 申请职位
        click('#resultList > div.dw_tlc > div.op > span.but_sq > i')
        # 关闭弹窗(刷新页面)
        browser.refresh()
        # 输入页数
        input_keys('#jump_page', page_num)
        # 点击确定按钮
        click('#resultList > div.dw_page > div > div > div > span.og_but')



    except TimeoutException:
        next_page(page_num)


# # css文本输入
def input_keys(selector, keys):
    input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
    input.clear()
    input.send_keys(keys)


# css点击
def click(selector):
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
    button.click()


def main():
    login()
    page_size = int(search())
    for i in range(2, page_size + 1):
        next_page(i)



if __name__ == '__main__':
    main()
