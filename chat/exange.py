import requests
from bs4 import BeautifulSoup

# 要爬取的网站链接
website_url = 'https://www.mylanguageexchange.com/search.asp?selX3=1&selX6=12&selCountry=null&txtCity=&txtAgeMin=&txtAgeMax=&selGender=0&selIsClass=null&selX4=null&selTxtChat=null&selX13=null&selFace=null&txtFName=&txtDesc=&selOrder=0&txtSrchName=&nRows=10&BtnSubSrch=Search'


def fetch_website_info(url):
    try:
        # 发起HTTP请求
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        proxy = {'http': '127.0.0.1:7890', 'https': '127.0.0.1:7890'}

        response = requests.get(url, headers=headers, proxies=proxy)
        response.raise_for_status()  # 检查是否请求成功
        content = response.content

        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(content, 'html.parser')

        td_elements = soup.select("table.TblDataRecs.TblSrchResults tbody")
        for td in td_elements:
            print(td.get_text().strip())  # 使用 .get_text() 方法来获取元素的文本内容

        return {

        }
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None


# 调用函数获取网站信息
if __name__ == '__main__':
    print()
    website_info = fetch_website_info(website_url)
    if website_info:
        print("Website Title:", website_info['title'])
        print("Links:")
        for link in website_info['links']:
            print(link)
