import scrapy

from WebScraper.items import WebscraperItem

class MicrocenterSpider(scrapy.Spider):
    name = "MicroCenter"
    allowed_domains = ["www.microcenter.com"]
    start_urls = ["https://www.microcenter.com/category/4294966661/headphones-and-earbuds"]

    def parse(self, response):
        for product in response.css("li.product_wrapper"):
            item = WebscraperItem()
            item["url"] = response.urljoin(product.css("div.result_left > a.image2 productClickItemV2::attr(href)").get())
            item["name"] = product.css("div.result_left > a::data-name(title)").get()
            item["current_price"] = product.css("div.result_right > div.price_wrapper > div.price > span::text").get()
            item["regular_price"] = product.css("div.result_right > div.price_wrapper > div.price > strike::text").get()
            item["stock"] = product.css("div.result_right > div.price_wrapper > div.stock > span.inventoryCnt::text").get()
            yield item
