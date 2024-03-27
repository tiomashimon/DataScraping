import scrapy


class HotlineSpider(scrapy.Spider):
    name = 'hotline_spider'
    allowed_domains = ['hotline.ua']
    start_urls = ['https://hotline.ua/ua/auto/avtoshiny-i-motoshiny/']

    def parse(self, response):
        # Знаходимо всі елементи, які містять посилання на товари
        for link in response.xpath('//a[contains(@href, "/auto-avtoshiny-i-motoshiny/")]'):
            product_link = link.xpath('@href').get()
            if not product_link.startswith('https://hotline.ua'):
                product_link = 'https://hotline.ua' + product_link
            yield response.follow(product_link, callback=self.parse_product, meta={'product_link': product_link})

    def parse_product(self, response):
        product_link = response.meta['product_link']
        shop_names = response.xpath('//a[@class="shop__title"]/text()').getall()
        shop_links = response.xpath('//a[@class="shop__title"]/@href').getall()

        product_item = {
            'product_link': product_link,
            'shops': []
        }

        for shop_name, shop_link in zip(shop_names, shop_links):
            if not shop_link.startswith('https://hotline.ua'):
                shop_link = 'https://hotline.ua' + shop_link
            product_item['shops'].append({
                'shop_name': shop_name.strip() if shop_name else None,
                'shop_link': shop_link if shop_link else None
            })

        yield product_item
