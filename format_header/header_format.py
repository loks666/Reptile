import re
headerStr = '''

Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9,ru;q=0.8
Connection: keep-alive
content-encoding: gzip
Content-Length: 6094
content-type: application/x-ndjson
Host: appsa.lagou.com
Origin: https://www.lagou.com
Referer: https://www.lagou.com/
sec-ch-ua: ".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-site
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36

'''
ret = ""
for i in headerStr:
    if i == '\n':
        i = "',\n'"
    ret += i
ret = re.sub(": ", "': '", ret)
print(ret[3: -3])
