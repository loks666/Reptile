# -*- coding: utf-8 -*-
# author:Gary
import csv
import json
import sys
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context
import requests  # 获取网页内容
from bs4 import BeautifulSoup  # 解析网页内容

# 获取网页的内容
from lxml import etree

session = requests.session()
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,ru;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'gravatar=images%2Fnone.jpg%3Faabb90b74fcc8ca2819178850c2a27ca; username=jax; phone=16621370084; mail=284190056%40qq.com; password=3369d4e61137f46fc0750552377743cb; https_waf_cookie=4b298858-77ce-4134fa046acee5f3c9ceaf61d0d489bca261; Hm_lvt_96901db7af1741c2fd2d52f310d78eaa=1647599297; Hm_lvt_c4dd741ab3585e047d56cf99ebbbe102=1647599389; Hm_lpvt_c4dd741ab3585e047d56cf99ebbbe102=1647599389; Hm_lpvt_96901db7af1741c2fd2d52f310d78eaa=1647600462; _dx_captcha_cid=14828343; _dx_uzZo5y=edc326160ff89339a68193cd4b791cf8ecfe7779217874315f7416da6ff9921dc01158a4; _dx_app_5157233da7fa2b042f57a03a578281c0=62346354cbjOVpvwX57AqseL7lhNXHzJuguAW3h1; _dx_captcha_vid=0D112B1C50BE02FB650413377ACEBF825E82B11009E42F14420B9B0393EA67533C3C84AAF08C4B53DB742A63C84AEE750F69FAF990940CE631C57100AE80845159834A7B802D89A633AF23FC77FCD517',
    'Host': 'proxy.ip3366.net',
    'Referer': 'https://proxy.ip3366.net/user/',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
}


# 从json文件中获取代理信息，如果文件或获取为空，就重新创建
def open_file_proxies():
    # noinspection PyBroadException
    try:
        with open("proxies.txt", 'r') as file:
            data = json.loads(file.read())
            print(data)
    except Exception as e:
        print(e)
        return {}
    if data is None:
        return {}
    else:
        return data


def get_free_proxies():
    url = "https://proxy.ip3366.net/free/"
    res = session.get(url)
    # 前面省略，从下面直奔主题，举个代码例子：
    print(res.text)


def remove_null(param_list):
    while '' in param_list:
        param_list.remove('')
    return param_list


def get_proxies():
    global proxies
    if 'http' in proxies.keys():
        http_list = proxies['http']
    else:
        http_list = []
    if 'https' in proxies.keys():
        https_list = proxies['https']
    else:
        https_list = []
    # http
    for i in range(2000):
        url1 = "http://dev.qydailiip.com/api/?apikey=874df86c53e50488a155a1c96982ba448fc284bc&num=1000&type=json&line=win&proxy_type=putong&sort=4&model=all&protocol=http&address=&kill_address=&port=&kill_port=&today=false&abroad=1&isp=&anonymity="
        res1 = session.get(url1)
        tmp = remove_null(json.loads(res1.text))
        http_list = http_list + tmp
        time.sleep(5)

    # https
    for i in range(2000):
        url2 = "http://dev.qydailiip.com/api/?apikey=874df86c53e50488a155a1c96982ba448fc284bc&num=1000&type=json&line=win&proxy_type=putong&sort=4&model=all&protocol=https&address=&kill_address=&port=&kill_port=&today=false&abroad=1&isp=&anonymity="
        res2 = session.get(url2)
        tmp = remove_null(json.loads(res2.text))
        https_list = https_list + tmp
        time.sleep(5)
    # 前面省略，从下面直奔主题，举个代码例子：
    # http = '//' + res.text.strip()
    proxies['http'] = http_list
    proxies['https'] = https_list
    print(proxies)
    json_str = json.dumps(proxies, indent=4)
    with open("proxies.txt", 'a+') as json_file:
        json_file.write(json_str)
    print("加载入文件完成...")
    # https = '//' + res.text.strip()
    # proxies_str = {
    #     'http': http,
    #     'https': https
    # }
    # print('代理信息：' + str(proxies_str))
    return proxies


proxies = open_file_proxies()
if not proxies:
    get_proxies()


def post_job(job_info):
    url = 'https://i.51job.com/delivery/delivery.php?rand=0.658666866743314&jsoncallback=jQuery183020401877146455116_1646912559272&jobid=({}%3A1_0)&prd=search.51job.com&prp=sou_sou_soulb&cd=search.51job.com&cp=search_list&resumeid=&cvlan=&coverid=&qpostset=&elementname=delivery_jobid_{}&deliverytype=1&deliverydomain=%2F%2Fi.51job.com&language=c&imgpath=%2F%2Fimg01.51jobcdn.com&_=1646912565703'
    for job in job_info:
        url = url.format(job['岗位id'], job['岗位id'])
        res = session.get(url, headers=header)
        # 获取网页，并带有伪装的浏览器头，一般好的网站会有检测是不是程序访问
        soup = BeautifulSoup(res.text, 'lxml')
        begin_index = soup.text.find('html:"') + len('html:"')
        end_index = soup.text.find('"', begin_index)
        result = soup.text[begin_index:end_index].strip()
        if "申请中包含已申请过的职位" in result:
            result = "已申请！"
        if "投递成功" in result:
            result = "投递成功!"
        msg = '岗位-' + job['岗位id'] + '==' + job['公司名'] + '==' + job['岗位名'] + '==' + job['公司类型'] + '==' + job[
            '公司人数'] + '==' + job['工资'] + '==' + str(job['JD简介']) + '==' + job['岗位地址'] + ': ' + result
        print(msg)
        with open('post.csv', 'a+', newline='') as student_file:
            writer = csv.writer(student_file)
            writer.writerow([job['岗位id'], job['公司名'], job['岗位名'], job['公司类型'], job[
                '公司人数'], job['工资'], str(job['JD简介']), job['岗位地址'], result])


def get_job_ids(num):
    url = 'https://search.51job.com/list/020000,000000,0000,00,9,99,{},2,{}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='.format(
        'java', num)
    res = session.get(url, headers=header, proxies=get_proxies())
    # 获取网页，并带有伪装的浏览器头，一般好的网站会有检测是不是程序访问
    res.encoding = res.apparent_encoding  # 设置编码，防止乱码
    html = etree.HTML(res.text)
    text = html.xpath('//script[@type="text/javascript"]/text()')
    job_data = list(text)
    if job_data is None:
        pass
    result = job_data[0]
    return result


def get_free_proxies():
    url = "http://proxy.ip3366.net/free/?action=china&page=101"
    res = session.get(url)
    print(res.text)
    pass


def assembly_param(data):
    data = data.replace("window.__SEARCH_RESULT__ =", "")
    data = json.loads(data)
    print(data)
    result = []
    # 热门
    if data['top_ads']:
        hot = data['top_ads'][0]
        hot_info = {'岗位id': hot['jobid'], '公司名': hot['company_name'], '岗位名': hot['job_name'],
                    '公司类型': hot['companytype_text'], '公司人数': hot['companysize_text'], '工资': hot['providesalary_text'],
                    'JD简介': hot['attribute_text'], '岗位地址': hot['job_href']}
        print(hot_info)
        result.append(hot_info)
    # 急招
    if data['auction_ads']:
        hurry = data['auction_ads'][0]
        hurry_info = {'岗位id': hurry['jobid'], '公司名': hurry['company_name'], '岗位名': hurry['job_name'],
                      '公司类型': hurry['companytype_text'], '公司人数': hurry['companysize_text'],
                      '工资': hurry['providesalary_text'],
                      'JD简介': hurry['attribute_text'], '岗位地址': hurry['job_href']}
        result.append(hurry_info)
    # 推广
    if data['market_ads']:
        market = data['market_ads'][0]
        market = {'岗位id': market['jobid'], '公司名': market['company_name'], '岗位名': market['job_name'],
                  '公司类型': market['companytype_text'], '公司人数': market['companysize_text'],
                  '工资': market['providesalary_text'],
                  'JD简介': market['attribute_text'], '岗位地址': market['job_href']}
        result.append(market)
    # 每页
    if data['market_ads']:
        engine = data['engine_jds']
        for item in engine:
            engine_jd = {'岗位id': item['jobid'], '公司名': item['company_name'], '岗位名': item['job_name'],
                         '公司类型': item['companytype_text'], '公司人数': item['companysize_text'],
                         '工资': item['providesalary_text'],
                         'JD简介': item['attribute_text'], '岗位地址': item['job_href']}
            result.append(engine_jd)
    return result


def test_post(id):
    url = 'https://i.51job.com/delivery/delivery.php?rand=0.658666866743314&jsoncallback=jQuery183020401877146455116_1646912559272&jobid=({}%3A1_0)&prd=search.51job.com&prp=sou_sou_soulb&cd=search.51job.com&cp=search_list&resumeid=&cvlan=&coverid=&qpostset=&elementname=delivery_jobid_{}&deliverytype=1&deliverydomain=%2F%2Fi.51job.com&language=c&imgpath=%2F%2Fimg01.51jobcdn.com&_=1646912565703'.format(
        id, id)
    res = session.get(url, headers=header, proxies=get_proxies())
    # 获取网页，并带有伪装的浏览器头，一般好的网站会有检测是不是程序访问
    print(res)


if __name__ == '__main__':
    print()
    print(proxies['http'])
    print(proxies['https'])
    # for i in range(1, 500):
    #     data = get_job_ids(i)
    #     with open('proxies.txt', encoding="utf-8") as f:
    #         data = f.read()
    #     jobs = assembly_param(data)
    #     if jobs:
    #         post_job(jobs)

    # test_post('138745002')
    # get_proxies()
