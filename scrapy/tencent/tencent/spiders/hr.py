import scrapy


class HrSpider(scrapy.Spider):
    name = 'hr'
    allowed_domains = ['tencent.com']
    start_urls = ['http://careers.tencent.com/position.php']

    def parse(self, response):
        print(response.text)
        a_list = response.xpath("//a[@class='recruit-list-link']")
        print(a_list)
        for a in a_list:
            item = {}
            item["title"] = a.xpath("./h4.text()").extract_first()
            item["post"] = a.xpath("./p[0].text()").extract_first()
            item["description"] = a.xpath("./p[1].text()").extract_first()
            yield item
            print(item)

