import re
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import os

chromedriver = "chromedriver.exe"
os.environ["webdriver.Chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.maximize_window()

url = 'https://login.51job.com/login.php'
wait = WebDriverWait(driver, 10)
xpath = 'xpath'
weibo_name = '284190056@qq.com'
weibo_psw = 'Lx284190056'


def weibo_login():
    url = 'https://login.51job.com/open/opentransit.php?openfrom=wb&url='
    driver.get(url)
    # click('//*[@id="userId"]')
    input_keys('//*[@id="userId"]', weibo_name, xpath)
    input_keys('.//*[@id="passwd"]', weibo_psw, xpath)
    click('.//*[@node-type="submit"]', xpath)
    # time.sleep(3)


def job_login():
    url = 'https://www.51job.com/'
    driver.get(url)
    input_keys('#loginname', '你的账号')
    input_keys('#password', '你的密码')
    click('#login_btn')


def search():
    try:
        # 点击首页
        click('//*[@id="topIndex"]/div/p/a[1]', xpath)
        # 搜索职位
        input_keys('//*[@id="kwdselectid"]', 'java开发', xpath)
        click('/html/body/div[3]/div/div[1]/div/button', xpath)
        # 获取页数
        page = driver.find_element_by_xpath(
            '//*[@class="td"]').text
        print(page)
        page = re.findall("\d+", page)[0]
        return int(page)
    except TimeoutException:
        return search()


def next_page(page_num):
    try:
        # 全选
        click_xpath('//*[@id="top_select_all_jobs_checkbox"]')
        # 申请职位
        # click_xpath('//*[@id="resultList"]/div[2]/div[2]/span[1]/i')
        click('//*[@id="resultList"]/div[3]/div[2]/span[1]', xpath)
        # 关闭弹窗(刷新页面)
        driver.refresh()
        # 输入页数
        input_keys('//*[@id="jump_page"]', page_num, xpath)
        # 点击确定按钮
        click_xpath('//*[@class="p_in"]/span[3]')

    except TimeoutException:
        next_page(page_num)


# css文本输入
def input_keys(selector, keys):
    input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
    input.clear()
    input.send_keys(keys)


# xpath文本输入
def input_keys(selector, keys, type):
    input = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
    input.clear()
    input.send_keys(keys)


# css点击
def click(selector, type):
    if type is None:
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
        button.click()
    else:
        button = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
        button.click()


# xpath点击
def click_xpath(selector):
    button = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
    button.click()


def input_keys_xpath(selector, keys):
    input = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
    input.clear()
    input.send_keys(keys)


def main():
    weibo_login()
    page_size = search()
    for i in range(2, page_size + 1):
        next_page(i)


if __name__ == '__main__':
    main()
