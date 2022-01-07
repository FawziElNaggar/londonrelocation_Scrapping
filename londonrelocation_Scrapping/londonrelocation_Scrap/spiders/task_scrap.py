import scrapy
from ..items import TaskItem

class TaskScrapSpider(scrapy.Spider):
    name = 'rental_scrap'
    allowed_domains = ['londonrelocation.com']
    start_urls = ['https://londonrelocation.com/properties-to-rent/']
    page_number = 1

    def parse(self, response):
        for start_url in self.start_urls:
            yield scrapy.Request(url=start_url,
                                 callback=self.parse_area)

    def parse_area(self, response):
        pages = response.xpath('.//div[contains(@class,"area-box-pdh")]//h4/a/@href').extract()

        for page in pages:
            yield scrapy.Request(url=page,
                                  callback=self.pagination)

    def pagination(self, response):
        for i in [1, 2, 3, 4, 5]:
            page_number = response.url+'&pageset='+str(i)
            yield scrapy.Request(url=page_number,
                                 callback=self.individual_property)

    def individual_property(self, response):
        x = response.xpath('/html/body/section/div/div[*]/div/div/div[2]/div/div[2]/div[1]/h4/a/@href').extract()
        for indv in x:
            yield scrapy.Request(url='https://londonrelocation.com'+indv,
                                 callback=self.final_property)

    def final_property(self, response):
        items = TaskItem()

        link = response.url
        items["link"] = link
        title = response.xpath('/html/body/section[1]/div/div[2]/div/div/div/div/h1/text()').extract()[0]
        items["title"] = title
        price = response.xpath('/html/body/section[1]/div/div[2]/div/div/div/div/h3/text()').extract()[0]
        salary = float(price.split()[0][1:])
        items["price"] = salary

        yield items
