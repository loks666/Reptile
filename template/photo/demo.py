# -*- coding: utf-8 -*-
# author:Gary
import csv
import json
import sys
import time

import requests  # 获取网页内容
from bs4 import BeautifulSoup  # 解析网页内容

# 获取网页的内容
from lxml import etree

session = requests.session()
header = {
    'Accept': 'text.txt/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'partner=www_baidu_com; privacy=1646901513; guid=525a26680b65dbdc7d66ac5731ba94d4; _ujz=MTE5ODA5MDY4MA%3D%3D; ps=needv%3D0; 51job=cuid%3D119809068%26%7C%26cusername%3DoCb1tjRgY6YJfZhC%252BaGbiHdHTJVz6A83g3hiq91DlS0%253D%26%7C%26cpassword%3D%26%7C%26cname%3DBqsrJLJyQv%252FpAXXFE9gutw%253D%253D%26%7C%26cemail%3DJ5%252BFrwLJnPDCk0J9ULel1WbaLINjrGFAS1NCfZJ%252B%252Bss%253D%26%7C%26cemailstatus%3D3%26%7C%26cnickname%3D%26%7C%26ccry%3D.0E32uEq7S%252Fps%26%7C%26cconfirmkey%3DsusZmAPbfBWbA%26%7C%26cautologin%3D1%26%7C%26cenglish%3D0%26%7C%26sex%3D0%26%7C%26cnamekey%3DsuwuP%252FdZxo6D.%26%7C%26to%3D456eb4d89dd23b760fe32bae830511ac6229b910%26%7C%26; slife=lowbrowser%3Dnot%26%7C%26lastlogindate%3D20220310%26%7C%26securetime%3DV2sGMwNhBWdeNVRqWGIBb1RlATY%253D; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; search=jobarea%7E%60000000%7C%21ord_field%7E%600%7C%21recentSearch0%7E%60000000%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA0%A1%FB%A1%FA%D3%CE%CF%B7%A1%FB%A1%FA2%A1%FB%A1%FA1%7C%21',
    'Host': 'search.51job.com',
    'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
}


def post_job(job_info):
    url = 'https://i.51job.com/delivery/delivery.php?rand=0.658666866743314&jsoncallback=jQuery183020401877146455116_1646912559272&jobid=({}%3A1_0)&prd=search.51job.com&prp=sou_sou_soulb&cd=search.51job.com&cp=search_list&resumeid=&cvlan=&coverid=&qpostset=&elementname=delivery_jobid_{}&deliverytype=1&deliverydomain=%2F%2Fi.51job.com&language=c&imgpath=%2F%2Fimg01.51jobcdn.com&_=1646912565703'
    for job in job_info:
        # time.sleep(1)
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


def get_proxies():
    url = "http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=1&pack=221347&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions="
    res = session.get(url)
    if '请2秒后再试' in res.text:
        time.sleep(2)
        get_proxies()
    # print('获取http ip为：' + res.text.txt)
    http = '//' + res.text.strip()
    time.sleep(2)
    url = "http://webapi.http.zhimacangku.com/getip?num=1&type=1&pro=&city=0&yys=0&port=11&pack=221347&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions="
    res = session.get(url)
    if '请2秒后再试' in res.text:
        time.sleep(2)
        get_proxies()
    # print('获取https ip为：' + res.text.txt)
    https = '//' + res.text.strip()
    proxies = {
        'http': http,
        'https': https
    }
    print('代理信息：' + str(proxies))
    return proxies


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
    for i in range(1, 500):
        data = get_job_ids(i)
        # with open('test.txt', encoding="utf-8") as f:
        #     data = f.read()
        jobs = assembly_param(data)
        if jobs:
            post_job(jobs)

    # test_post('138745002')
    # get_proxies()
