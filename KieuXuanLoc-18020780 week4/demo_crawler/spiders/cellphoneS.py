import scrapy
import csv
import re
from datetime import datetime

class TgddSpider(scrapy.Spider):
    name = 'cellphoneS'
    allowed_domains = ['cellphones.com.vn']
    start_urls = ['https://cellphones.com.vn/']
    CRAWLED_COUNT = 0
    total_page = set()
    csv_columns = ['link', 'name', 'rating', 'category', 'price', 'promotion_infor',
                   'introduction', 'short_description', 'specification']
    with open("C:/Users/Admin/Downloads/KieuXuanLoc-18020780/output/news/cellphoneS.csv", mode="a+",
              encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=csv_columns)
        writer.writeheader()
    def parse(self, response):
        csv_columns = ['link', 'name', 'rating', 'category', 'price', 'promotion_infor',
                       'introduction', 'short_description', 'specification']
        if response.status == 200 and response.css('div::attr(class)').get() == 'wrapper':
            print('Crawling from:', response.url)
            data = {
                'link': response.url,

                'name': response.css('div.topview h1::text').get(),
                'rating': response.css('p.averageRatings::text').get(),
                'category': '/ '.join([
                    ''.join(c.css('*::text').getall()) for c in response.css('div.breadcrumbs > ul > li > a')
                ]),
                'price': response.css('p.special_price > span::text').get(),

                'promotion_infor': '\n'.join([
                    ''.join(c.css('*::text').getall())
                    for c in response.css('div.kmChung h4::text')
                ]),

                'introduction': response.css('meta[property="og:description"]::attr(content)').get(),

                'short_description': ','.join([
                    ''.join(c.css('*::text').getall())
                    for c in response.css('ul.configurable_swatch_color span')
                ]),

                'specification':
                    ''.join([
                        ''.join(c.css('*::text').getall())
                        for c in response.css('div.blog-content p')
                    ]),

            }

            data['category'] = data['category'].replace('Trang chủ', '')

            with open('C:/Users/Admin/Downloads/KieuXuanLoc-18020780/output/news/cellphoneS1.csv', mode="a+", encoding='utf8') as f:
                writer = csv.DictWriter(f, fieldnames=csv_columns, delimiter=',')
                writer.writerow(data)
                self.CRAWLED_COUNT += 1
                self.crawler.stats.set_value('CRAWLED_COUNT', self.CRAWLED_COUNT)
                print('SUCCESS:', response.url)

        yield from response.follow_all(
            css='a[href^="https://cellphones.com.vn/"]::attr(href), a[href^="/"]::attr(href)', callback=self.parse)