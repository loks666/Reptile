import json

import lxml.html
from lxml import etree
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait


def init_driver(index):
    global driver
    options = webdriver.FirefoxOptions()
    geckodriver_path = r'geckodriver.exe'
    service = Service(geckodriver_path)
    driver = webdriver.Firefox(options=options, service=service)
    # 获取副屏的分辨率（假设副屏是第二个屏幕）
    screen_width = driver.execute_script("return window.screen.width;")
    screen_height = driver.execute_script("return window.screen.height;")

    # 将浏览器窗口移动到副屏
    driver.set_window_position(screen_width, 0)

    # 最大化浏览器窗口
    driver.maximize_window()
    # 打开网页
    driver.get(index)
    return driver


# 点击元素
def click(xpath):
    button = driver.find_element(By.XPATH, xpath)
    button.click()


# 填写字符
def send_keys(xpath, text):
    button = driver.find_element(By.XPATH, xpath)
    button.send_keys(text)


def saveData(data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        for item in data:
            file.write(item + '\n')


def wait_element(xpath):
    while True:
        element = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, xpath)))
        if element:
            break


if __name__ == '__main__':
    # url = "https://www.zhipin.com/chengshi/c101170400/"
    url = 'https://www.zhipin.com/web/geek/job?query=Java&city=101020100'
    # 初始化 driver
    driver = init_driver(url)
    data_list = []  # 创建一个空列表
    # click("//a[@ka='header-login']")  # 点击登录
    # click("/html/body/div/div/div[2]/div[2]/div[1]")  # 点击扫码登录
    # wait_element("//a[@ka='header-home']")    # 等待首页元素出现
    # driver.get("https://www.zhipin.com/web/geek/job?query=Java&city=101020100")
    # wait_element('//ul[@class="job-list-box"]')
    # 读取HTML文件

    html = driver.page_source

    # 使用lxml解析HTML
    parsed_html = lxml.html.fromstring(html)
    # 找到ul元素
    # Find the ul element
    ul_element = parsed_html.xpath('//ul[@class="job-list-box"]/text()')

    # Check if ul_element is not empty
    if ul_element:
        # Extract the text content from ul_element
        ul_text = ul_element[0]

        # Process ul_text to find li elements
        # For example, you can split the text content into individual lines
        lines = ul_text.split('\n')

        # Find the li elements within the ul_text content
        for line in lines:
            if "job-card-wrapper" in line:
                # Process the li element, extract information as needed
                li_element = lxml.html.fromstring(line)
                job_info = {
                    "公司名称": li_element.xpath('.//div[@class="company-name"]/a')[0].text,
                    "所处行业": li_element.xpath('.//ul[@class="company-tag-list"]/li[1]')[0].text,
                    "岗位标签": li_element.xpath('.//ul[@class="tag-list"]/li[1]')[0].text,
                    "薪资范围": li_element.xpath('.//span[@class="salary"]')[0].text,
                    # Add more fields as needed
                }
                data_list.append(job_info)



    # # 遍历li元素
    # for li_element in li_elements:
    #     job_info = {"公司名称": li_element.xpath('.//div[@class="company-name"]/a').text,
    #                 "所处行业": li_element.xpath('.//ul[@class="company-tag-list"]/li[1]')[0].text,
    #                 "岗位标签": li_element.xpath('.//ul[@class="tag-list"]/li[1]')[0].text,
    #                 "薪资范围": li_element.xpath('.//span[@class="salary"]')[0].text,
    #                 "融资情况": li_element.xpath('.//ul[@class="company-tag-list"]/li[2]')[0].text,
    #                 "人员规模": li_element.xpath('.//ul[@class="company-tag-list"]/li[3]')[0].text,
    #                 "年限要求": li_element.xpath('.//ul[@class="tag-list"]/li[1]')[0].text,
    #                 "学历要求": li_element.xpath('.//ul[@class="tag-list"]/li[3]')[0].text,
    #                 "岗位名称": li_element.xpath('.//div[@class="job-title"]/span[@class="job-name"]')[0].text,
    #                 "岗位地址": li_element.xpath('.//div[@class="job-area-wrapper"]/span[@class="job-area"]')[0].text,
    #                 "公司福利": li_element.xpath('.//div[@class="info-desc"]')[0].text,
    #                 "公司链接": li_element.xpath('.//div[@class="company-logo"]/a')[0].get('href'),
    #                 "发布人员": li_element.xpath('.//a[@class="start-chat-btn"]')[0].text,
    #                 "联系人": li_element.xpath('.//div[@class="info-public"]')[0].text}
    #
    #     print(job_info)
    #     data_list.append(job_info + '\n')

    # 将内容保存到 txt 文件
    saveData(data_list, "data.txt")

    # driver.quit()
