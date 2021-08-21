import requests
import re
import threading
import os
import random
import socket
import struct
import time

########################################
phone = "16621370084"
########################################
# 短信接口API 请求间隔时间 备注 请求方式 请求参数 需要SESSION的先决请求URL以及Referer
APIList = [
    # ["https://login.ceconline.com/thirdPartLogin.do",60,"世界经理人","POST",{"mobileNumber":phone,"method": "getDynamicCode","verifyType": "MOBILE_NUM_REG","captcharType":"","time": str(int(time.time()*1000))},""],

    # ["http://www.ntjxj.com/InternetWeb/SendYzmServlet",120,"机动车手机绑定","POST",{"sjhm" : phone},"http://www.ntjxj.com/InternetWeb/regHphmToTel.jsp"],

    # ["https://www.itjuzi.com/api/verificationCodes",60,"IT橘子","POST",{"account": phone},""],

    # ["http://yifatong.com/Customers/gettcode",60,"易法通","GET",{"rnd": ("%0.3f" % (time.time())),"mobile":phone},"http://yifatong.com/Customers/registration?url="],

    # ["http://qydj.scjg.tj.gov.cn/reportOnlineService/login_login",60,"天津企业登记","POST",{'MOBILENO': phone,'TEMP': 1},""],

    # ["http://www.shijiebang.com/a/mobile/vcode/",120,"世界邦","GET",{'key': phone},"http://www.shijiebang.com/reg/"],

    # ["http://www.yidaer2.com/api/sms/receive",60,"一戴二","GET",{'phone': phone},"http://www.yidaer2.com/register.html"],

    ["http://www.yidaer2.com/api/sms/receive", 60, "一戴二2", "POST", {'phone': phone},
     "http://www.yidaer2.com/register.html"],

    [
        "http://reg.ztgame.com/common/sendmpcode?source=giant_site&nonce=&type=verifycode&token=&refurl=&cururl=http://reg.ztgame.com/&mpcode=&pwd=&tname=&idcard=",
        60, "巨人网络", "GET", {'phone': phone}, "http://reg.ztgame.com/"],

    # ["http://www.homekoo.com/zhixiao/zt_baoming_ajax_pc_new.php",180,"尚品宅配","POST",{"action":"OK","username":"吕布","tel":phone,"qq":"","province":"","city":"","kehu_tel_time":"","tg_id":"296","sp_type":"986","num_id":"5","zhuanti_pages":"http://www.homekoo.com/zhixiao/cuxiao/index.php","prevurl":""},"http://www.homekoo.com/zhixiao/cuxiao/index.php"],

    # ["http://jrh.financeun.com/Login/sendMessageCode3.html",60,"金融号","GET",{"mobile":phone,"mbid":"197858"},"http://jrh.financeun.com/Login/jrwLogin?web=jrw"],

    # ["https://www.decathlon.com.cn/zh/ajax/rest/model/atg/userprofiling/ProfileActor/send-mobile-verification-code",30,"迪卡侬","POST",{"countryCode":"CN","mobile":phone},"https://www.decathlon.com.cn/zh/create"],

    # ["http://cta613.org/sendsms.php",60,"支教","POST",{"y":"1","sj":phone},""],

    # ["http://sns.qnzs.youth.cn/ajax/passportSendSms",120,"青年之声","POST",{"mobile":phone},"http://sns.qnzs.youth.cn/user/passport"]

]

########################################


if __name__ == '__main__':
    phone = '16621370084'
    url = 'http://passport.sunlands.com/randCodeNew.action'
    data = {
"mobile":"16621370084",
"userValidateCode":"vvnk",
"type":"registor",
"currentTime":"1598280768345",
"codeSign":"b86d949869bda2fd65da6479ab51a096",
}
    # 字符串格式
    res = requests.post(url=url, data=data)
    print(res.content)
    # response = requests.post('https://id.ifeng.com/api/checkMobile?callback=jQuery18304042834512414408_1598279372985',
    #                          '16621370184')
    # print(response.content)
    # print(response.status_code)
