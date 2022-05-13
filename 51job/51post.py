import os
import re
import sys
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

s = Service(executable_path=r'chromedriver.exe')
browser = webdriver.Chrome(service=s)
browser.set_window_position(3841, 0)
browser.maximize_window()
url = 'https://login.51job.com/login.php?loginway=0&isjump=0&lang=c&from_domain=i&url='
wait = WebDriverWait(browser, 10)


def login():
    browser.get(url)
    input_keys('//*[@id="loginname"]', '16621370084')
    input_keys('//*[@id="password"]', 'l284190056')
    click('//*[@class="check"]')
    time.sleep(1)
    click('//*[@id="login_btn_withPwd"]')
    time.sleep(1)


def get_image_url(self, xpath):
    link = re.compile(
        'background-image: url\("(.*?)"\); width: 30px; height: 100px; background-position: (.*?)px (.*?)px;')
    elements = self.driver.find_elements_by_xpath(xpath)
    image_url = None
    location = list()
    for element in elements:
        style = element.get_attribute("style")
        groups = link.search(style)

        url = groups[1]
        x_pos = groups[2]
        y_pos = groups[3]

        location.append((int(x_pos), int(y_pos)))
        image_url = url
    return image_url, location


def get_page():
    # post = 'https://search.51job.com/list/020000,000000,0000,00,9,99,java,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
    post = 'https://search.51job.com/list/020000,000000,0000,00,9,99,java%25E5%25BC%2580%25E5%258F%2591,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
    browser.get(post)
    page_num = wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div/div[1]/div[2]/div[1]'))).text
    # print('page is :' + page_num)
    return int(page_num.split('/')[-1].strip())


def send_post():
    # noinspection PyBroadException
    try:
        click('/html/body/div[2]/div[3]/div/div[1]/div[1]/span[1]/em')
        click('/html/body/div[2]/div[3]/div/div[1]/div[2]/div[2]/button[2]')
        time.sleep(2)
        browser.refresh()
        click('//a[@class="e_icons i_next"]')
    except Exception:
        send_post()


# css文本输入
def input_keys(selector, keys):
    inputs = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
    inputs.clear()
    inputs.send_keys(keys)


# 点击
def click(selector):
    button = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
    button.click()


if __name__ == '__main__':
    login()
    page = get_page()
    print(page)
    for i in range(1, page):
        print('正在投递 第 {} 页的职位。。。'.format(i))
        send_post()
    print('投递完毕！')
    browser.quit()
    os.system('shutdown /s /t 0')
