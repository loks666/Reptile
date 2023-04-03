# ------------------------------------------------------------------------
# 本脚本具有自动下载猎聘网职位信息，并完成搜索、下载、筛选，提交职位的功能，需要注册猎聘网账号，并完成简历填写
# 原理：requests爬取关键字相关搜索结果->使用pandas本地筛选->使用selenium模拟登录->使用opencv识别验证码->使用selenium模拟提交职位
# opencv识别部分：https://blog.csdn.net/Tracy_LeBron/article/details/84567419
# ------------------------------------------------------------------------
import requests
import re
import os
import time
import pandas as pd
import sys
import cv2
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options


class LiePin:
    def __init__(self):
        self.try_num = 0  # 当前网页请求重试次数
        self.total_page = 0  # 搜索页面总页数
        requests.packages.urllib3.disable_warnings()
        self.islogin = False
        self.post_num = 0
        pass

    def get_html(self, url, type_="text"):
        # 获取一个网页的页面信息， 有3次重连机会
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0"}
        try:
            r = requests.get(url, headers=headers, verify=False)
            print(r)
        except:
            print("网页连接错误，再次尝试")
            r = self.get_html(url)
        if r.status_code == 200:
            self.try_num = 0
            r.encoding = r.apparent_encoding
            if type_ == "text":
                return r.text
            else:
                return r.content
        else:
            if self.try_num <= 3:
                self.try_num = self.try_num + 1
                print("获取网页信息失败：第 %d 次重连-----: %s" % (self.try_num, url))
                time.sleep(1)
                self.get_html(url)
            else:
                self.try_num = 0
                print("获取网页信息失败 --------: %s" % url)
                return None

    def gen_urls(self, key):
        # 检索搜索关键字的页面数，并生成url
        base_url = "https://www.liepin.com/zhaopin/?init=-1&fromSearchBtn=2&degradeFlag=0&key=%s&d_sfrom=search_unknown&d_pageSize=40"
        # base_url = "https://c.liepin.com/?time=1680542042166"
        test_url = base_url % key
        test_html = self.get_html(test_url)
        if test_html is not None:
            max_num = re.search(r'<a class="last".+?&curPage=(\d+).+?title="末页">', test_html)
            if max_num:
                max_num = int(max_num.group(1))
                self.total_page = max_num + 1
                if max_num > 0:
                    return [test_url + "&curPage=" + str(i) for i in range(max_num + 1)]
                else:
                    # 搜索结果只有一页
                    return test_url
            else:
                print("生成url失败：%s" % key)
                return None
        else:
            print("生成url失败：%s" % key)
            return None

    def parser_position(self, url, position_infos):
        # 爬取具体某一页的职位信息
        if not "position_num" in position_infos.keys():
            position_infos["position_num"] = 0
        html = self.get_html(url)
        if html is not None:
            # 职位名称
            position_names = re.findall(r'<div class="job-info">[\d\D]+?<h3 title="(.+?)"', html)
            # 职位待遇和要求：工资，地点，学历，经验
            position_conditions = re.findall(r'<p class="condition clearfix"[\d\D]+?title="(.+?)"', html)
            # 发布时间
            position_post_times = re.findall(r'time-info clearfix"[\d\D]+?time title="(.+?)"', html)
            # 公司名称
            company_names = re.findall(r'company-name"[\d\D]+?<a title="(.+?)"', html)
            # company_financing = re.findall(r'field-financing[\d\D]+?<span>(.+?)</span>', html)
            # 具体职位要求链接
            position_details = re.findall(r'job-info[\d\D]+?<a href="(.+?)"', html)

            for i in range(len(position_names)):
                conditions = position_conditions[i].split("_")
                # 具体url地址处理， 有的链接加上域名
                if position_details[i].startswith("/a"):
                    new_detail = "https://www.liepin.com/" + position_details[i]
                else:
                    new_detail = position_details[i]
                # 薪资处理， 将工资分为最小薪资，最大薪资，是否有12/13/14薪
                if "面议" == conditions[0]:
                    min_salary = "面议"
                    max_salary = "面议"
                    two_weeks_salary = "面议"
                else:
                    a = conditions[0].split("·")
                    if len(a) == 1:
                        two_weeks_salary = None
                    else:
                        two_weeks_salary = a[1]
                    b = a[0].split("-")
                    if len(b) == 1:
                        min_salary = 1000 * int(b[0][:-1])
                        max_salary = 1000 * int(b[0][:-1])
                    else:
                        min_salary = 1000 * int(b[0])
                        max_salary = 1000 * int(b[1][:-1])

                position_info = {}
                position_info["position_name"] = position_names[i][2:]
                position_info["min_salary"] = min_salary
                position_info["max_salary"] = max_salary
                position_info["two_weeks_salary"] = two_weeks_salary
                position_info["address"] = conditions[1]
                position_info["degree"] = conditions[2]
                position_info["experience"] = conditions[3]
                position_info["post_time"] = position_post_times[i]
                position_info["company"] = company_names[i][2:]

                position_info["position_detail"] = new_detail

                position_infos[position_infos["position_num"] + 1] = position_info
                position_infos["position_num"] = position_infos["position_num"] + 1

    def parser(self, key):
        # 爬取所有职位信息
        urls = self.gen_urls(key)
        info = {}
        k = 1
        for url in urls:
            sys.stdout.write("\r正在爬取-%s-相关职位信息：%d/%d--%s" % (key, k, self.total_page, url))
            sys.stdout.flush()
            self.parser_position(url, info)
            k = k + 1
            time.sleep(1)
        # 简单处理信息， 转为dataframe并存储
        if len(info):
            info.pop("position_num")
            info = pd.DataFrame(info).T
            info = info.reindex(columns=[
                "position_name",
                "address",
                "min_salary",
                "max_salary",
                "two_weeks_salary",
                "degree",
                "experience",
                "company",
                "post_time",
                "position_detail"])
            info = info.drop_duplicates()
            info.to_csv("./%s.csv" % key)
            return info

    @staticmethod
    def filter_position(path, key, not_key, address, min_salary, degree, experience):
        degrees = ["学历不限", "中专/中技及以上", "大专及以上", "统招本科", "本科及以上", "硕士及以上", "博士",
                   "博士后"]
        experiences = ["^" + str(i) + "年以上" for i in range(20)]
        experiences.insert(0, "经验不限")
        info = pd.read_csv(path, sep=",", index_col=0)

        # 职位关键字筛选
        info = info[info["position_name"].str.contains("|".join(key))]
        info = info[~info["position_name"].str.contains("|".join(not_key))]
        # 工作地点筛选
        info = info[info["address"].str.contains("|".join(address))]
        # 学历筛选
        if degree == "中专":
            index = 2
        elif degree == "大专":
            index = 3
        elif degree == "本科":
            index = 5
        elif degree == "研究生":
            index = 6
        elif degree == "博士":
            index = 7
        elif degree == "博士后":
            index = 7
        else:
            index = 1
        personal_degree = "|".join(degrees[0:index])
        info = info[info["degree"].str.contains(personal_degree)]
        # 经验筛选
        experience = "^" + str(experience) + "年以上"
        index = experiences.index(experience)
        info = info[info["experience"].str.contains("|".join(experiences[0:index + 1]))]

        # 工资筛选
        # 面议
        info_1 = info[info["min_salary"].str.contains("面议")]
        # 具体工资
        info_2 = info[~info["min_salary"].str.contains("面议")]
        info_2 = info_2[info_2["min_salary"].astype(float) >= min_salary]
        info_2 = info_2[info_2["min_salary"].astype(float) <= 15000]
        info = pd.concat([info_2, info_1])
        # 保存
        new_path = "/".join(path.split("/")[0:-1]) + "/filtered_" + path.split("/")[-1]
        info.to_csv(new_path)
        return info

    def gen_driver(self):
        opt = Options()
        opt.add_argument('--headless')
        driver = webdriver.Firefox(options=opt)
        self.driver = driver
        self.driver.maximize_window()

    def login(self, account, password):
        print("开始模拟登录。。。")
        url = "https://www.liepin.com/"
        self.driver.get(url)
        try:
            password_login_button = WebDriverWait(
                driver=self.driver, timeout=20, poll_frequency=0.5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[2]/div/div/div[1]/span[2]')))
            password_login_button.click()
            time.sleep(1)
            account_form = WebDriverWait(
                driver=self.driver, timeout=20, poll_frequency=0.5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[2]/div/div/div[2]/div/section[2]/div/form/div[1]/input')))
            password_form = WebDriverWait(
                driver=self.driver, timeout=20, poll_frequency=0.5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[2]/div/div/div[2]/div/section[2]/div/form/div[2]/input')))
            login_button = WebDriverWait(
                driver=self.driver, timeout=20, poll_frequency=0.5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '/html/body/div[2]/div/div/div[2]/div/section[2]/div/form/input[2]')))

            account_form.send_keys(account)
            time.sleep(1)
            password_form.send_keys(password)
            time.sleep(1)
            login_button.click()
            time.sleep(3)
            self.driver.switch_to.frame('tcaptcha_iframe')
            WebDriverWait(
                driver=self.driver, timeout=20, poll_frequency=0.5).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="tcWrap"]')))
            time.sleep(3)
            background_url = self.driver.find_element_by_xpath('//*[@id="slideBg"]').get_attribute("src")
            block_url = self.driver.find_element_by_xpath('//*[@id="slideBlock"]').get_attribute("src")
            with open("./background.jpg", "wb") as f:
                f.write(self.get_html(background_url, type_="pic"))
            with open("./block.jpg", "wb") as f:
                f.write(self.get_html(block_url, type_="pic"))
            self.verify()
            self.driver.refresh()
            time.sleep(3)
            html = self.driver.page_source
            res = re.search(r'我的首页_猎聘', html)
            if res:
                print("模拟登录成功")

                cookies = self.driver.get_cookies()
                self.driver.delete_all_cookies()
                for cookie in cookies:
                    for k in {'name', 'value', 'domain', 'path', 'expiry'}:
                        if k not in list(cookie.keys()):
                            if k == 'expiry':
                                t = time.time()
                                cookie[k] = int(t)  # 时间戳s
                    self.driver.add_cookie({k: cookie[k] for k in {'name', 'value', 'domain', 'path', 'expiry'}})
                self.islogin = True
                return cookies
            else:
                print("模拟登录失败，再次尝试")
                self.login(account, password)
        except:
            print("模拟登录失败，再次尝试")
            self.login(account, password)

    def get_distance(self, bkg, blk):
        block = cv2.imread(blk)
        template = cv2.imread(bkg)

        block = cv2.cvtColor(block, cv2.COLOR_BGR2GRAY)
        block = abs(255 - block)
        cv2.imwrite('block.jpg', block)
        block = cv2.imread('block.jpg')

        result = cv2.matchTemplate(block, template, cv2.TM_CCOEFF_NORMED)
        x, y = np.unravel_index(result.argmax(), result.shape)
        # 这里就是下图中的绿色框框
        cv2.rectangle(template, (y + 20, x + 20), (y + 136 - 25, x + 136 - 25), (7, 249, 151), 2)
        # 之所以加20的原因是滑块的四周存在白色填充
        return y, template

    @staticmethod
    def get_tracks(distance, dis):
        v = 10
        t = 1
        # 保存0.3内的位移
        tracks = []
        current = 0
        mid = distance * 3 / 4
        while current <= dis:
            if current < mid:
                a = 2
            else:
                a = -8
            v0 = v
            v = v0 + a * t
            s = v0 * t + 0.5 * a * t * t
            current += s
            tracks.append(round(s))
        return tracks

    def verify(self):
        distance, te = self.get_distance("./background.jpg", "./block.jpg")
        double_distance = int((distance - 70 + 20) / 2)

        tracks = self.get_tracks(distance, double_distance)
        # 由于计算机计算的误差，导致模拟人类行为时，会出现分布移动总和大于真实距离，这里就把这个差添加到tracks中，也就是最后进行一步左移。
        tracks.append(-(sum(tracks) - double_distance))

        element = self.driver.find_element_by_id('tcaptcha_drag_thumb')

        ActionChains(self.driver).click_and_hold(on_element=element).perform()
        # ActionChains(self.driver).reset_actions()
        for track in tracks:
            ActionChains(self.driver).move_by_offset(xoffset=track, yoffset=0).perform()
        # ActionChains(self.driver).reset_actions()
        time.sleep(0.5)
        ActionChains(self.driver).release(on_element=element).perform()
        time.sleep(3)

    def post_position(self, position_urls, account, password, history_path=None):
        if not self.islogin:
            cookies = self.login(account, password)

        # print(cookies)
        if history_path is None:
            history = set()
        else:
            if os.path.exists(history_path):
                with open(history_path, "r", encoding="utf-8") as f:
                    history_urls = f.readlines()
                    history = set([i.strip() for i in history_urls])
            else:
                history = set()
        for url in position_urls:
            if self.post_num >= 50:  # 每天最多提交50个
                break
            if url in history:
                continue

            self.driver.get(url)
            if not re.search(r'btn btn-warning btn-apply-disabled', self.driver.page_source):
                try:
                    position_button = WebDriverWait(
                        driver=self.driver, timeout=20, poll_frequency=0.5).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//a[@class="btn-apply btn btn-warning"]')))
                    position_button.click()
                    time.sleep(1)
                    send_button = WebDriverWait(
                        driver=self.driver, timeout=20, poll_frequency=0.5).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '/html/body/div[7]/div[2]/div[2]/div/form/div[2]/input[1]')))
                    send_button.click()
                    # 记录提交的个数
                    self.post_num = self.post_num + 1
                    print("%d: %s职位已提交" % (self.post_num, url))
                    time.sleep(1)
                except:
                    print("%s提交失败" % url)
                    self.post_position(position_urls, account, password, history_path="history.txt")
            else:
                print("该职位已经提交过%s" % url)
            history.add(url)
            with open("./history.txt", "w", encoding="utf-8") as f:
                a = list(history)
                a = [i + "\n" for i in a]
                f.writelines(a)
            time.sleep(1)
        self.driver.close()
        pass


if __name__ == "__main__":
    search_keys = ["Java开发"]  # 需修改
    lp = LiePin()

    for key in search_keys:
        lp.parser(key)  # 爬取职位信息 本地有爬取的信息可以跳过
    infos = []
    for key in search_keys:
        # 信息过滤
        info = lp.filter_position(
            path="./%s.csv" % key,  # 下载的本地文件路径
            key=search_keys,  # 职位包含的关键字，可以多个  需修改
            not_key=["总监", "负责人", "科学家", "销售", "专家", "java", "JAVA", "经理"],  # 职位中不包含的关键字
            address=["上海", "杭州", "北京", "重庆", "苏州"],  # 地点包含的关键字，可以多个  需修改
            min_salary=8000,  # 最低工资，结果中包含最低工资及以上和面议  需修改
            degree="本科",  # 你的学历  需修改（中专，大专，本科，研究生，博士，博士后）
            experience=1  # 工作经验（年）  需修改（0-20）
        )
        infos.append(info)
    infos = pd.concat(infos)
    # 职位具体页面链接
    position_urls = list(infos["position_detail"])
    # 生成driver
    lp.gen_driver()
    # 提交
    lp.post_position(
        position_urls,  # 待提交职位url
        account="",  # 账号  需修改
        password="",  # 密码  需修改
        history_path="history.txt"  # 已提交职位历史记录
    )
