# -*- coding: utf-8 -*-
import random
import six
import os, base64
import time, re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import requests
import io
from io import BytesIO
import cv2


class qjh(object):
    def __init__(self):
        s = Service(executable_path=r'chromedriver.exe')
        driver = webdriver.Chrome(service=s)
        self.wait = WebDriverWait(driver, 10)
        self.driver = driver
        self.driver.set_window_size(1440, 900)

    def core(self):
        # url = "http://www.pkulaw.cn/cluster_form.aspx?Db=chl&menu_item=law&EncodingName=&clust_param=0/XC02&keyword=&range=name&"
        url = 'https://login.51job.com/login.php?loginway=0&isjump=0&lang=c&from_domain=i&url='
        self.driver.get(url)

        # input = WebDriverWait(self.driver, 10).until(
        #     EC.presence_of_element_located((By.XPATH, '//*[@id="gopage1"]'))
        # )
        input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="loginname"]'))
        )
        input.send_keys('16621370084')

        input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="password"]'))
        )
        input.send_keys('l284190056')
        time.sleep(1)
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@class="check"]')))
        button.click()
        time.sleep(4)
        button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="login_btn_withPwd"]')))
        button.click()
        time.sleep(5)  # 等待加载
        cut_image_url, cut_location = self.get_image_url('//canvas[@class="geetest_canvas_bg geetest_absolute"]')
        cut_image = self.mosaic_image(cut_image_url, cut_location)
        cut_image.save("./code/cut.jpg")

        self.driver.execute_script(
            "var x=document.getElementsByClassName('xy_img_bord')[0];"
            "x.style.display='block';"
        )
        cut_fullimage_url = self.get_move_url('//div[@class="xy_img_bord"]')
        resq = base64.b64decode(cut_fullimage_url[22::])

        file1 = open('./code/2.jpg', 'wb')
        file1.write(resq)
        file1.close()

        res = self.FindPic("./code/cut.jpg", "./code/2.jpg")

        res = res[3][0]  # x坐标

        self.start_move(res)

    def FindPic(self, target, template):
        """
        找出图像中最佳匹配位置
        :param target: 目标即背景图
        :param template: 模板即需要找到的图
        :return: 返回最佳匹配及其最差匹配和对应的坐标
        """
        target_rgb = cv2.imread(target)
        target_gray = cv2.cvtColor(target_rgb, cv2.COLOR_BGR2GRAY)
        template_rgb = cv2.imread(template, 0)
        res = cv2.matchTemplate(target_gray, template_rgb, cv2.TM_CCOEFF_NORMED)
        value = cv2.minMaxLoc(res)
        return value

    def get_move_url(self, xpath):
        # 得到滑块的位置
        link = re.compile(
            'background-image: url\("(.*?)"\); ')  # 严格按照格式包括空格
        elements = self.driver.find_elements_by_xpath(xpath)
        image_url = None

        for element in elements:
            style = element.get_attribute("style")
            groups = link.search(style)
            url = groups[1]
            image_url = url
        return image_url

    def get_image_url(self, xpath):
        # 得到背景图片

        url = 'https://api.geetest.com/refresh.php?gt=a0ae9818c05923219e1430323079cbf4&challenge=b7ab9b733989cc06372ed9488b27de45gg&lang=zh-cn&type=multilink&callback=geetest_1648306235456'
        self.driver.get(url)
        link = re.compile(
            'background-image: url\("(.*?)"\); width: 30px; height: 100px; background-position: (.*?)px (.*?)px;')  # 严格按照格式包括空格
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

    # 拼接图片
    def mosaic_image(self, image_url, location):

        resq = base64.b64decode(image_url[22::])
        file1 = open('./code/1.jpg', 'wb')
        file1.write(resq)
        file1.close()
        with open("./code/1.jpg", 'rb') as f:
            imageBin = f.read()
        # 很多时候，数据读写不一定是文件，也可以在内存中读写。
        # BytesIO实现了在内存中读写bytes，创建一个BytesIO，然后写入一些bytes：
        buf = io.BytesIO(imageBin)
        img = Image.open(buf)
        image_upper_lst = []
        image_down_lst = []
        count = 1
        for pos in location:
            if pos[0] > 0:
                if count <= 10:
                    if pos[1] == 0:

                        image_upper_lst.append(img.crop((abs(pos[0] - 300), 0, abs(pos[0] - 300) + 30, 100)))
                    else:
                        image_upper_lst.append(img.crop((abs(pos[0] - 300), 100, abs(pos[0] - 300) + 30, 200)))
                else:
                    if pos[1] == 0:

                        image_down_lst.append(img.crop((abs(pos[0] - 300), 0, abs(pos[0] - 300) + 30, 100)))
                    else:
                        image_down_lst.append(img.crop((abs(pos[0] - 300), 100, abs(pos[0] - 300) + 30, 200)))
            elif pos[0] <= -300:

                if count <= 10:
                    if pos[1] == 0:

                        image_upper_lst.append(img.crop((abs(pos[0] + 300), 0, abs(pos[0] + 300) + 30, 100)))
                    else:
                        image_upper_lst.append(img.crop((abs(pos[0] + 300), 100, abs(pos[0] + 300) + 30, 200)))
                else:
                    if pos[1] == 0:

                        image_down_lst.append(img.crop((abs(pos[0] + 300), 0, abs(pos[0] + 300) + 30, 100)))
                    else:
                        image_down_lst.append(img.crop((abs(pos[0] + 300), 100, abs(pos[0] + 300) + 30, 200)))
            else:
                if count <= 10:
                    if pos[1] == 0:

                        image_upper_lst.append(img.crop((abs(pos[0]), 0, abs(pos[0]) + 30, 100)))
                    else:
                        image_upper_lst.append(img.crop((abs(pos[0]), 100, abs(pos[0]) + 30, 200)))
                else:
                    if pos[1] == 0:

                        image_down_lst.append(img.crop((abs(pos[0]), 0, abs(pos[0]) + 30, 100)))
                    else:
                        image_down_lst.append(img.crop((abs(pos[0]), 100, abs(pos[0]) + 30, 200)))
            count += 1
        x_offset = 0
        # 创建一张画布，x_offset主要为新画布使用
        new_img = Image.new("RGB", (300, 200))
        for img in image_upper_lst:
            new_img.paste(img, (x_offset, 0))
            x_offset += 30

        x_offset = 0
        for img in image_down_lst:
            new_img.paste(img, (x_offset, 100))
            x_offset += 30

        return new_img

    def start_move(self, distance):
        element = self.driver.find_element_by_xpath('//div[@class="handler handler_bg"]')
        # 按下鼠标左键
        ActionChains(self.driver).click_and_hold(element).perform()
        time.sleep(0.5)
        while distance > 0:
            if distance > 10:
                # 如果距离大于10，就让他移动快一点
                span = random.randint(10, 15)
            else:
                # 快到缺口了，就移动慢一点
                span = random.randint(2, 3)
            ActionChains(self.driver).move_by_offset(span, 0).perform()
            distance -= span
            time.sleep(random.randint(10, 50) / 100)

        ActionChains(self.driver).move_by_offset(distance, 1).perform()
        ActionChains(self.driver).release(on_element=element).perform()


if __name__ == "__main__":
    h = qjh()
    h.core()
