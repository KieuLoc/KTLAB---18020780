import scrapy
import json
import re
from datetime import datetime

class TgddSpider(scrapy.Spider):
    name = 'cellphoneS'
    allowed_domains = ['cellphones.com.vn']
    start_urls = ['https://cellphones.com.vn/']
    CRAWLED_COUNT = 0

    def parse(self, response):
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

                # 'sale_price': response.css('div.box-online > div > strong:text').get(),
                # 'end_date_sale': response.css('div.box-online > div > div::attr(data-time)').get(),

                'promotion_infor': '\n'.join([
                    ''.join(c.css('*::text').getall())
                    for c in response.css('div.kmChung h4::text')
                ]),

                'list_img_src': response.css('meta[name="url"]::attr(content)').get(),

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

            with open('C:/Users/Admin/Downloads/ExampleCode/output/news/TGDD2', 'a', encoding='utf8') as f:
                f.write(json.dumps(data, ensure_ascii=False))
                f.write('\n')
                self.CRAWLED_COUNT += 1
                self.crawler.stats.set_value('CRAWLED_COUNT', self.CRAWLED_COUNT)
                print('SUCCESS:', response.url)

        yield from response.follow_all(
            css='a[href^="https://cellphones.com.vn/"]::attr(href), a[href^="/"]::attr(href)', callback=self.parse)