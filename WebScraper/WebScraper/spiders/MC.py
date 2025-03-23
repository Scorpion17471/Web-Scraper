import scrapy

from WebScraper.items import WebscraperItem

class McSpider(scrapy.Spider):
    name = "MC"
    allowed_domains = ["www.microcenter.com"]
    start_urls = ["https://www.microcenter.com/category/4294966661/headphones-and-earbuds"]

    def parse(self, response):
        for product in response.css("li.product_wrapper"):
            item = WebscraperItem()
            # Direct Product URL
            item["url"] = response.urljoin(product.css("div.result_left > a.image2::attr(href)").get())
            # Product Name as Listed
            item["name"] = product.css("div.result_left > a::attr(data-name)").get()
            # Current Price/Regular Price if not on sale
            item["current_price"] = product.css("div.price > span::text").get()
            # Regular Price if on sale, returns None if not on sale
            item["regular_price"] = product.css("div.price > div.standardDiscount > strike::text").get()
            # Current inventory count (Scraper is only looking for in stock items right now)
            item["stock"] = product.css("div.stock > span.inventoryCnt::text").get()
            yield item

        next_page = response.css("ul.pages > li:last-child > a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)