import re

headerStr = '''
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,ru;q=0.8
Cache-Control: max-age=0
Connection: keep-alive
Cookie: channelid=0; sid=1647833513314527; _ga=GA1.2.1486380935.1647835097; _gid=GA1.2.1973847089.1647835097; Hm_lvt_7ed65b1cc4b810e9fd37959c9bb51b31=1647835097; _gcl_au=1.1.469411156.1647835102; _gat=1; Hm_lpvt_7ed65b1cc4b810e9fd37959c9bb51b31=1647835235
Host: www.kuaidaili.com
Referer: https://www.baidu.com/link?url=XgTbbyU_rsasv9AjmGK-Dx0cH3X7HPgzeA8Pv_AP-B4WEl6wHFOmUQUQemuZFHhn&wd=&eqid=d7ac94e2000007be000000046237f7db
sec-ch-ua: " Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: cross-site
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36
'''
ret = ""
for i in headerStr:
    if i == '\n':
        i = "',\n'"
    ret += i
ret = re.sub(": ", "': '", ret)
print(ret[3: -3])

