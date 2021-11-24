import requests
from PIL import Image
from pytesseract import image_to_string

auth_code = 'auth_code.png'
session = requests.session()


#  获取验证码
def get_auth_code():
    global session
    session.get('http://biz.smpaa.cn/ysxtqxcp/')
    response = session.get('http://biz.smpaa.cn/ysxtqxcp/myCaptcha')
    with open(auth_code, 'wb') as f:
        f.write(response.content)


# 图片转变中度灰，识别不出
def convert_img():
    img = Image.open(auth_code)
    imgry = img.convert('L')
    binary = imgry.point(get_bin_table(), '1')
    binary.save('binary.png')
    text = image_to_string(img)
    print(text)


# 降噪，转换效果不理想
def get_bin_table(threshold=115):
    """
    获取灰度转二值的映射table
    0表示黑色,1表示白色
    """
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table


# 图片二值化
def two_value():
    im = Image.open(auth_code)
    # 图像二值化
    data = im.getdata()
    w, h = im.size
    black_point = 0

    for x in range(1, w - 1):
        for y in range(1, h - 1):
            mid_pixel = data[w * y + x]  # 中央像素点像素值
            if mid_pixel < 50:  # 找出上下左右四个方向像素点像素值
                top_pixel = data[w * (y - 1) + x]
                left_pixel = data[w * y + (x - 1)]
                down_pixel = data[w * (y + 1) + x]
                right_pixel = data[w * y + (x + 1)]

                # 判断上下左右的黑色像素点总个数
                if top_pixel < 10:
                    black_point += 1
                if left_pixel < 10:
                    black_point += 1
                if down_pixel < 10:
                    black_point += 1
                if right_pixel < 10:
                    black_point += 1
                if black_point < 1:
                    im.putpixel((x, y), 255)
                # print(black_point)
                black_point = 0

    im.save('test.png')


# 识别验证码
def discern_code():
    img = Image.open(auth_code)
    text = image_to_string(img)
    print(text)


def get_buy_data():
    global session
    url = 'http://biz.smpaa.cn/ysxtqxcp/cpcx/hcxx/queryCgd/yq'
    headers = {
        'Accept': 'text/plain, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '100',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Cookie': 'JSESSIONID=OP57pL9NmjTBQwbLzOiNkaXtoyVH-Wb0N1zy5SAjL8MqV4VnPMCi!-2060801452',
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
    response = session.post(url, headers=headers, data=form_data)
    with open('data.txt', 'w') as f:
        f.write(response.text)
    print(response.text)


def login():
    global session
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '50',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'biz.smpaa.cn',
        'Origin': 'http://biz.smpaa.cn',
        'Pragma': 'no-cache',
        'Referer': 'http://biz.smpaa.cn/ysxtqxcp/login.jsp',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36',
    }
    data = {'loginName': '', 'password': '', 'captcha': input('验证码：')}
    session.post('http://biz.smpaa.cn/ysxtqxcp/login', headers=headers, data=data)


if __name__ == '__main__':
    get_auth_code()
    login()
    get_buy_data()
