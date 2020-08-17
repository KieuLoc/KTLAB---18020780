import scrapy
from datetime import datetime
import csv

class Kenh14TestSpider(scrapy.Spider):
    name = 'zingnews'
    allowed_domains = ['zingnews.vn']
    start_urls = ['https://zingnews.vn/']
    CRAWLED_COUNT = 0
    total_page = set()
    csv_columns = ['link', 'title', 'author', 'summary', 'category', 'tags', 'content']
    with open("C:/Users/Admin/Downloads/KieuXuanLoc-18020780/output/news/FPT.csv", mode="a+", encoding='utf-8') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=csv_columns)
        writer.writeheader()

    def parse(self, response):
        csv_columns = ['link', 'title', 'author', 'summary', 'category', 'tags', 'content']
        if response.status == 200:
            print('Crawling from: ' + response.url)
            data = {
                'link': response.url,
                'title': response.css('h1.the_article_title::text').get(),
                'author': response.css('li.the-article-author::text').get(),
                'summary': response.css('p.the-article-summary::text').get(),
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

            with open('C:/Users/Admin/Downloads/KieuXuanLoc-18020780/output/news/newZinggg.csv', 'a', encoding='utf8') as f:
                writer = csv.DictWriter(f, fieldnames=csv_columns, delimiter=',')
                writer.writerow(data)
                self.CRAWLED_COUNT += 1
                self.crawler.stats.set_value('CRAWLED_COUNT', self.CRAWLED_COUNT)
                print('SUCCESS:', response.url)

        yield from response.follow_all(css='a[href^="/"]::attr(href)', callback=self.parse)