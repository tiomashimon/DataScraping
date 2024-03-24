import scrapy
import json
from urllib.parse import urljoin

class URLSpider(scrapy.Spider):
    name = "url_spider"
    
    def __init__(self, url=None, *args, **kwargs):
        super(URLSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]

    def parse(self, response):
        # Отримання базового URL сторінки
        base_url = response.url
        
        # Отримання всіх посилань зі сторінки
        urls = response.css('a::attr(href)').getall()
        
        # Обробка неповних URL-адрес
        complete_urls = [urljoin(base_url, url) for url in urls]
        
        for url in complete_urls:
            yield scrapy.Request(
                url="http://127.0.0.1:8000/api/urls/",
                method='POST',
                body=json.dumps({"url": url}),
                headers={'Content-Type': 'application/json'},
                callback=self.parse_post_response
            )

    def parse_post_response(self, response):
        if response.status == 200:
            self.logger.info("URL successfully sent: %s", response.body)
        else:
            self.logger.error("Failed to send URL: %s", response.body)
