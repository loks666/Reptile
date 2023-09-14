import requests, time, json, csv
import pymysql
from urllib.parse import urlencode
from bs4 import BeautifulSoup

list_data = []
csv_data = []


# 发送请求页面并存下数据
def spider_boss(url, data, ):
    req = requests.post(url, headers=headers, data=data, timeout=5, ).text
    list = json.loads(req)
    if 'jobList' not in list['zpData'].keys():
        print('cookie过期请更换...')
        exit()
    try:
        for i in list['zpData']['jobList']:
            title = i['jobName']  # 职业信息
            jobDegree = i['jobDegree']  # 学历
            brandName = i['brandName']  # 公司名称
            areaDistrict = i['areaDistrict'] + i['businessDistrict']  # 地区加地址
            salaryDesc = i['salaryDesc']  # 工资
            jobExperience = i['jobExperience']  # 经验
            urladdr = 'https://www.zhipin.com/job_detail/' + i['encryptJobId'] + '.html'  # url地址
            skills = ','.join(i['skills'])  # 工作内容
            welfareList = ','.join(i['welfareList'])  # 公司福利
            mag = {
                'title': title,
                'jobDegree': jobDegree,
                'brandName': brandName,
                'areaDistrict': areaDistrict,
                'salaryDesc': salaryDesc,
                'jobExperience': jobExperience,
                'urladdr': urladdr,
                'skills': skills,
                'welfareList': welfareList,
            }
            list_data.append(mag)
        print(list_data)
        return list_data
    except:
        print('请检查cookies是否过期...')
        time.sleep(2)
        spider_boss(url, data)


# 储存mysql数据库
def server(data):
    # 连接数据库
    con = pymysql.connect(host='127.0.0.1', user='root', password='root', db='boss', charset='utf8')
    cursor = con.cursor()
    for conter in data:
        try:
            sql = "INSERT INTO heji(title,jobDegree,brandName,areaDistrict,salaryDesc,jobExperience,urladdr,skills,welfareList) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                conter['title'], conter['jobDegree'], conter['brandName'], conter['areaDistrict'], conter['salaryDesc'],
                conter['jobExperience'], conter['urladdr'], conter['skills'], conter['welfareList'])
            cursor.execute(sql)
            con.commit()
        except:
            con.rollback()
            print('请检查sql语句..')
        print('数据库写入成功...')
    # 完成后关闭数据库
    con.close()


def server_csv(data):
    # 遍历数据，处理成存储数据
    for conter in data:
        csv_list = [conter['title'], conter['jobDegree'], conter['brandName'], conter['areaDistrict'],
                    conter['salaryDesc'], conter['jobExperience'], conter['urladdr'], conter['skills'],
                    conter['welfareList']]
        csv_data.append(csv_list)
    with open('求职信息.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['职业', '学历', '公司名称', '地区', '工资', '经验', 'url地址', '工作内容', '公司福利'])
        writer.writerows(csv_data)
        print('cvs表格写入成功..')


def strat(url, data):
    # 开启抓取页面
    list_data = spider_boss(url, data)
    # 储存mysql数据库
    # server(list_data)
    # 存储csv表格
    server_csv(list_data)


if __name__ == '__main__':
    # 目标网站url
    url = 'https://www.zhipin.com/wapi/zpgeek/recommend/job/list.json'
    # cookie更改 bug中，每次查询5次需要手动更换
    cookie = 'lastCity=101020100; __zp_seo_uuid__=a951c374-7d2f-413a-b55b-dee7f1edc0bc; __g=-; __l=r=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DnREKHj_58hX0AQCk54Xy5EyfeMk4XtLcCkjDybWN9V5ZoNwUxGTRMW6SlzIto4KR%26wd%3D%26eqid%3D87523add0017b0fa00000004644bce56&l=%2Fwww.zhipin.com%2Fshanghai%2F&s=1&g=&s=3&friend_source=0; wd_guid=4a2d8efd-b1d3-465d-bd13-c38815003333; historyState=state; boss_login_mode=app; wt2=DuPEPE6iW5yuJZEstqiSGfx0FeZEXEIs2ieZZ5bImK37BS_kuK853BdptzoLMTLGyZDsh6lMZkK-zID5WUJO3AQ~~; wbg=0; _bl_uid=2Ll1sh9b0Rwlnsy10fww6zkvvt92; geek_zp_token=V1R9MjEOX12lRrWt1ryRQYKymz6T7R; __c=1682689613; __a=93630902.1682689613..1682689613.4.1.4.4; __zp_stoken__=9171eKW8HUSBQX3h4dl5BFVFlYTk3UTctV0QtaQtxOlZ4byc6fCc0AVMrcQ4%2FKVpdLS5fNR01R39%2BR3RdYiBeUhVOHSBiU2RGUDliEkFQN3sASRthF2VdAQl2L216VRwWbxdtTmA8NwNBBno%3D; __zp_sseed__=b+iO5CHXI8wd46M7D/ZKQHHSIjmOddKV6PMB4W2Ya2o=; __zp_sname__=70c092c1; __zp_sts__=1682689689285'
    # 设置headers请求头信息
    headers = {
        "referer": "https://www.zhipin.com/web/geek/recommend?expectId=136314657&sortType=1&page=4&districtCode=0&cityCode=101280100",
        "cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
    }
    # 批量遍历页面url
    for num in range(1, 30):
        data = {
            "expectId": "136314657",
            "sortType": 1,
            "page": num,
            "salary": "",
            "payType": "",
            "degree": "",
            "experience": "",
            "stage": "",
            "scale": "",
            "districtCode": 0,
            "businessCode": "",
        }

        data = urlencode(data)
        strat(url, data)
