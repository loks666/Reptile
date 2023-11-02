import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import time


def init_driver():
    options = webdriver.FirefoxOptions()
    geckodriver_path = r'geckodriver.exe'
    service = Service(geckodriver_path)
    driver = webdriver.Firefox(options=options, service=service)
    return driver


def saveData(data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        for item in data:
            file.write(item + '\n')


# 下载文件
def download_file(download_path, file):
    with requests.get(download_path, stream=True) as response:
        response.raise_for_status()  # 检查请求是否成功
        with open(file, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)


if __name__ == '__main__':
    # 初始化 driver
    driver = init_driver()

    # 打开网页
    url = "https://www.pkulaw.com/lar/1c77b9ec949b7d8a6862a6c3676b3110bdfb.html"
    driver.get(url)

    data_list = []  # 创建一个空列表

    # 抓取信息
    content_text = driver.find_element(By.XPATH, '//div[@class="content"]').text
    data_list.append(content_text)

    # 抓取下载链接
    download_link = driver.find_element(By.XPATH, '//a[@class="fjLink"]')
    download_url = download_link.get_attribute("href")
    file_name = download_link.text

    data_list.append("文件名：" + file_name)
    data_list.append("下载地址：" + download_url)
    # 将内容保存到 txt 文件
    saveData(data_list, "data.txt")

    # 下载文件
    download_file(download_url, file_name)

    # 关闭浏览器
    driver.quit()
