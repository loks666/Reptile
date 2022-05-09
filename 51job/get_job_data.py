#!/usr/bin/python3.6
import json
import sys
import time
import datetime
from lxml import html, etree

import pymysql as pymysql
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ChromeOptions
import threading

s = Service(executable_path=r'chromedriver.exe')
# s = Service(executable_path=r'chromedriver')
options = ChromeOptions()
options.headless = True
options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)
browser = webdriver.Chrome(service=s, options=options)
browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": """
    Object.defineProperty(navigator, 'webdriver', {
      get: () => undefined
    })
  """
})

browser.maximize_window()
url = 'https://login.51job.com/login.php?loginway=0&isjump=0&lang=c&from_domain=i&url='
wait = WebDriverWait(browser, 10)


def login():
    browser.get(url)
    input_keys('//*[@id="loginname"]', 'zhanghuming')
    input_keys('//*[@id="password"]', 'mima')
    click('//*[@class="check"]')
    time.sleep(1)
    click('//*[@id="login_btn_withPwd"]')
    time.sleep(1)


def get_page(target):
    browser.get(target)
    page_num = wait.until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[3]/div/div[1]/div[2]/div[1]'))).text
    # print('page is :' + page_num)
    return int(page_num.split('/')[-1].strip())


def get_post_data(source):
    file = etree.HTML(source)
    text = file.xpath('//script[@type="text/javascript"]/text()')
    return text[0].replace("window.__SEARCH_RESULT__ =", "")


# css文本输入
def input_keys(selector, keys):
    inputs = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
    inputs.clear()
    inputs.send_keys(keys)


# 点击
def click(selector):
    button = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
    button.click()


post_list = []


def assembly_param(post_info):
    # 热门
    if post_info['top_ads']:
        add_info(post_info['top_ads'][0])
    # 急招
    if post_info['auction_ads']:
        add_info(post_info['auction_ads'][0])
    # 推广
    if post_info['market_ads']:
        add_info(post_info['market_ads'][0])
    # 每页
    if post_info['engine_jds']:
        engine = post_info['engine_jds']
        for item in engine:
            add_info(item)


def create_connector():
    # 连接数据库
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='Lx284190056',
        database='post',
        charset='utf8',
        # autocommit=True,    # 如果插入数据，， 是否自动提交? 和conn.commit()功能一致。
    )
    return conn


def get_joblist():
    con = create_connector()
    cur = con.cursor()
    cur.execute('Select job_id from post.51job')
    result = cur.fetchall()
    cur.close()
    con.close()
    jobs = []
    for job in result:
        # print(job[0])
        jobs.append(job[0])
    return jobs


joblist = get_joblist()


def add_info(raw):
    global joblist
    # print('jobid 为 ：' + raw['jobid'])
    if raw['jobid'] not in joblist:
        info = {'公司id': raw['coid'], '公司名': raw['company_name'], '公司类型': raw['companytype_text'],
                '公司人数': raw['companysize_text'],
                '工资': raw['providesalary_text'],
                '岗位名': raw['job_name'],
                '岗位id': raw['jobid'], '岗位类型': raw['type'],
                '公司福利': ','.join(raw['jobwelf_list']), '岗位要求': ','.join(raw['attribute_text']),
                '岗位url': raw['job_href'],
                '公司url': raw['company_href'], '更新时间': raw['issuedate']}
        post_list.append(info)
    else:
        pass


def insert_data():
    global joblist
    # 插入sql语句
    # sql = "insert into school (schoolId,schoolName,schoolNum,location,level,served) values (%s,%s,%s,%s,%s,%s)"
    sql = "INSERT INTO `post`.`51job`(`com_id`, `com_name`, `com_type`, `com_count`, `com_url`, `search_key`,`salary`, `job_name`, `job_id`, `job_type`, `job_benefits`, `job_req`, `job_url`, `base`, `area`, `update_time`, `insert_time`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s)"
    # 执行插入操作
    con = create_connector()
    cursor = con.cursor()
    for post in post_list:
        com_id = post['公司id']
        com_name = post['公司名']
        com_type = post['公司类型']
        com_count = post['公司人数']
        salary = post['工资']
        job_name = post['岗位名']
        job_id = post['岗位id']
        job_type = post['岗位类型']
        job_benefits = post['公司福利']
        job_req = post['岗位要求']
        split = job_req.split(',')
        city = split[0]
        if '-' in city:
            split = city.split('-')
            base = split[0]
            area = split[1]
        else:
            base = city
            area = city
        job_url = post['岗位url']
        com_url = post['公司url']
        # 2022-03-25 08:16:50
        # print(post['更新时间'])
        # update_time = datetime.time().strptime(post['更新时间'], '%Y-%m-%d %H:%M:%S')
        update_time = post['更新时间']
        insert_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        insert = cursor.execute(sql, (
            com_id, com_name, com_type, com_count, com_url, search_key, salary, job_name, job_id, job_type,
            job_benefits, job_req,
            job_url, base, area, update_time, insert_time))
        # print(insert)
        joblist.append(job_id)
    con.commit()  # 增加，修改，删除数据必须提交
    cursor.close()
    # 关闭数据库连接
    con.close()


def get_all_data(target, key):
    page = get_page(target)
    print('获取总页数为： ' + str(page))
    for i in range(page):
        print('正在获取第 ' + str(i + 1) + ' 页的数据…… ，共 ' + str(page) + '页！')
        print('目前已有岗位 ' + str(len(joblist)) + ' 条!')
        job_data = get_post_data(source=browser.page_source)
        if job_data is not None:
            data = json.loads(job_data)
            print('data为：' + str(data))
            # 组装数据
            assembly_param(data)
            # 插入数据库
            insert_data()
            post_list.clear()
        else:
            pass
        if i + 1 == page:
            browser.quit()
            sys.exit()
        click('//a[@class="e_icons i_next"]')
        time.sleep(1)
        browser.refresh()
        time.sleep(1)


url = 'https://search.51job.com/list/{},000000,0000,00,9,99,{},2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='


def multithreaded():
    # login()
    beijing = 'https://search.51job.com/list/010000,000000,0000,00,9,99,java,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
    shanghai = 'https://search.51job.com/list/020000,000000,0000,00,9,99,java,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
    guangzhou = 'https://search.51job.com/list/030200,000000,0000,00,9,99,java,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='
    shenzhen = 'https://search.51job.com/list/040000,000000,0000,00,9,99,java,2,1.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='

    print('thread %s is running...' % threading.current_thread().name)

    # thread_list = []
    # t1 = threading.Thread(target=get_all_data, args=(beijing,))
    # t2 = threading.Thread(target=get_all_data, args=(shanghai,))
    # t3 = threading.Thread(target=get_all_data, args=(guangzhou,))
    # t4 = threading.Thread(target=get_all_data, args=(shenzhen,))
    # thread_list.append(t1)
    # thread_list.append(t2)
    # thread_list.append(t3)
    # thread_list.append(t4)
    #
    # for t in thread_list:
    #     t.setDaemon(True)  # 设置为守护线程
    #     t.start()
    #     t.join()  # 在这个子线程完成运行之前，主线程将一直被阻塞
    # print('thread %s ended.' % threading.current_thread().name)


if __name__ == '__main__':
    all = '000000'
    search_key = 'java'
    url = url.format(all, search_key)
    get_all_data(url, search_key)
