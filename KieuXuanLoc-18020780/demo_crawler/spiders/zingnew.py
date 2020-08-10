import scrapy
import json
from datetime import datetime

OUTPUT_FILENAME = 'output/news/zingnews_{}.txt'.format(datetime.now().strftime('%Y%m%d_%H%M%S'))


class Kenh14TestSpider(scrapy.Spider):
    name = 'zingnews'
    allowed_domains = ['zingnews.vn']
    start_urls = ['https://zingnews.vn/']
    CRAWLED_COUNT = 0

    def parse(self, response):
        if response.status == 200:
            print('Crawling from: ' + response.url)
            data = {
                'link': response.url,
                'title': response.css('h1.the_article_title::text').get(),
                'author': response.css('li.the-article-author::text').get(),
                'sumary': response.css('p.the-article-summary::text').get(),
                'category': response.css('p.the-article-category a::text').get(),
                # 'image': response.css('div.VCSortableInPreviewMode active a::attr(href)').get(),

                'tags': response.css('span.tag-item a::text').getall(),

                # 'date': response.css('span.kbwcm-time::text').get(),

                # 'content': '\n'.join(response.css('div.knc-content p::text').getall())
                'content': '\n'.join([
                    ''.join(c.css('*::text').getall())
                    for c in response.css('div.the-article-body p')
                ]),

            }

            with open('C:/Users/Admin/Downloads/ExampleCode/output/news/newZing', 'a', encoding='utf8') as f:
                f.write(json.dumps(data, ensure_ascii=False))
                f.write('\n')
                self.CRAWLED_COUNT += 1
                self.crawler.stats.set_value('CRAWLED_COUNT', self.CRAWLED_COUNT)
                print('SUCCESS:', response.url)

        yield from response.follow_all(css='a[href^="/"]::attr(href)', callback=self.parse)