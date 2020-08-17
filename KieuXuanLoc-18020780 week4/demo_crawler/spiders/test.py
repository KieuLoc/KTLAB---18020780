import scrapy
import csv


class LaoDongSpider(scrapy.Spider):
    name = 'FPT'
    allowed_domains = ['fptshop.com.vn']
    start_urls = ['https://fptshop.com.vn/may-tinh-bang/ipad-pro-129-2020-wi-fi-4g-256gb',
                  'https://fptshop.com.vn/may-tinh-xach-tay/macbook-pro-16-touch-bar-23ghz-core-i9',
                  'https://fptshop.com.vn/dien-thoai/samsung-galaxy-z-flip']
    total_pages = set()
    csv_columns = ['Link', 'Title', 'Type', 'Current Price', 'Rate', 'Image', 'Specifications', 'Description']
    with open("C:/Users/Admin/Downloads/KieuXuanLoc-18020780/output/news/FPT.csv", mode="a+", encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=csv_columns)
        writer.writeheader()

    def parse(self, response):
        csv_columns = ['Link', 'Title', 'Type', 'Current Price', 'Rate', 'Image', 'Specifications', 'Description']

        dict = {
            'Link': response.url,
            'Title': response.css('h1::text').get(),
            'Type': response.css('ul.fs-breadcrumb li:nth-child(2) a::text').get(),
            'Current Price': ''.join(
                filter(str.isalnum, response.css('p.fs-dtprice::text,span.fs-gsocit strong::text').get())),
            # 'Original Price':response.css('p.fs-dtprice del::text').get(),
            'Rate': ''.join(filter(str.isalnum, response.css('div.fs-dtrt-col.fs-dtrt-c1 h5::text').get())),
            'Image': response.css('meta[property="og:image"]::attr("content")').get(),
            'Specifications': response.css('div.fs-tsright label::text,div.fs-tsright span::text').getall(),
            'Description': response.css('div.fs-dtctbox.fsdtcts.clearfix p::text').getall()

        }
        # response.css('p.fs-dtprice::text,span.fs-gsocit strong::text').get()
        # response.xpath('normalize-space(//span[@class="fs-gsocit"]/strong/text())').get()
        with open('C:/Users/Admin/Downloads/KieuXuanLoc-18020780/output/news/FPT.csv', mode="a+", encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=csv_columns, delimiter=',')
            writer.writerow(dict)

        for href in response.css('div.owl-carousel.fsicte.otherlazy.fsdsamesc a.related_item::attr(href)').getall():
            if len(self.total_pages) <= 200:
                self.total_pages.add(href)
                yield response.follow(href, callback=self.parse)
# Go to /spiders and run in command
# scrapy crawl FPT