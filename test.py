import requests

url = 'http://biz.smpaa.cn/ysxtqxcp/cpcx/hcxx/queryCgd/yq'

headers = {
    'Accept': 'text/plain, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Length': '100',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': 'JSESSIONID=OP57pL9NmjTBQwbLzOiNkaXtoyVH-Wb0N1zy5SAjL8MqV4VnPMCi!-2060801452',
    'Host': 'biz.smpaa.cn',
    'Origin': 'http://biz.smpaa.cn',
    'Pragma': 'no-cache',
    'Referer': 'http://biz.smpaa.cn/ysxtqxcp/menu?p=/pub/cpcx/cgd/cgdxxcx_yq&menuid=10202004&_t=348616&_winid=w2185',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

form_data = {
    'hcddmxid': '',
    'scqybm': '',
    'yybm': '',
    'psdbm': '',
    'cglx': '',
    'pm': '',
    'tjfs': '',
    'ddmxzt': '',
    'pageIndex': '1',
    'pageSize': '20',
    'sortField': '200'
}

resp = requests.post(url, headers=headers, data=form_data)
with open('test.txt', 'w') as f:
    f.write(resp.text)
print(resp.text)
print(len(resp.text))
