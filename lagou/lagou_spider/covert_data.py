import sys
import datetime

import pymysql

from lagou.lagou_spider.handle_insert_data import lagou_mysql


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


def covert():
    con = create_connector()
    # cur = con.cursor()
    cur = con.cursor(pymysql.cursors.DictCursor)
    cur.execute('Select * from post.`51job` where insert_time is not null and job_benefits is not null;')
    result = cur.fetchall()
    cur.close()
    con.close()
    return result


# def insert_data():
#     global joblist
#     # 插入sql语句
#     # sql = "insert into school (schoolId,schoolName,schoolNum,location,level,served) values (%s,%s,%s,%s,%s,%s)"
#     # 执行插入操作
#
#     for lagou in lagou_list:
#         lagou_list
#     insert = cursor.execute(sql, (
#         com_id, com_name, com_type, com_count, com_url, search_key, salary, job_name, job_id, job_type,
#         job_benefits, job_req,
#         job_url, base, area, update_time, insert_time))
#     print(insert)
#     con.commit()  # 增加，修改，删除数据必须提交
#     cursor.close()
#     # 关闭数据库连接
#     con.close()


if __name__ == '__main__':
    job_list = covert()
    lagou_list = []
    con = create_connector()
    cursor = con.cursor()
    # insert_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for job in job_list:
        print(job)
        lagou = {}
        split = job['job_req'].split(',')
        if len(split) < 3:
            continue
        city = split[0]
        lagou['id'] = job['job_id']
        lagou['positionName'] = job['area']
        lagou['workYear'] = split[1]
        lagou['education'] = split[2]
        lagou['jobNature'] = '全职'
        lagou['financeStage'] = '未知'
        lagou['companySize'] = job['com_count']
        lagou['industryField'] = '未知'
        lagou['city'] = job['base']
        lagou['companyShortName'] = job['base']
        lagou['companyFullName'] = job['base']
        lagou['district'] = job['area']
        lagou['companyLabelList'] = job['job_req']
        lagou['salary'] = job['salary']
        lagou['crawl_date'] = job['insert_time']
        lagou_list.append(lagou)

        sql = "INSERT INTO `lagou`.`lagou_data`(`id`, `positionID`, `longitude`, `latitude`, `positionName`, `workYear`, `education`, `jobNature`, `financeStage`, `companySize`, `industryField`, `city`, `positionAdvantage`, `companyShortName`, `companyFullName`, `district`, `companyLabelList`, `salary`, `crawl_date`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        insert = cursor.execute(sql, (
            job['job_id'], job['com_id'], 0, 0, job['job_name'], split[1], split[2], '全职', '未知', job['com_count'],
            job['com_type'], job['base'],
            job['job_benefits'], job['com_name'], job['com_name'], job['area'], job['job_req'], job['salary'],
            job['insert_time']))
        print(insert)
        # print(lagou_list)
    con.commit()  # 增加，修改，删除数据必须提交
    cursor.close()
    sys.exit()
    # print(covert())
