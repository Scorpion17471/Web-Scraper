import scrapy

from WebScraper.items import AMZItem

class AmzSpider(scrapy.Spider):
    name = "AMZ"
    allowed_domains = ["www.amazon.com"]
    start_urls = ["https://www.amazon.com/gp/browse.html?rw_useCurrentProtocol=1&node=12097478011&ref_=amb_link_wWKVXRlOSpW2CEglBx9yZg_1"]

    def parse(self, response):
        for product in response.css("div.s-asin"):
            item = AMZItem()
            # Direct Product URL
            item["url"] = response.urljoin(product.css("div.puis-list-col-right > div > div > div > a::attr(href)").get())
            # Product Name as Listed
            item["name"] = product.css("div.puis-list-col-right > div > div > div > a > h2::attr(aria-label)").get()
            # Current Price/Regular Price if not on sale - SECONDARY ORDERING CRITERIA
            item["current_price"] = product.css("span.a-price > span::text").get()
            # Regular Price if on sale, returns None if not on sale
            item["regular_price"] = product.css("div.puis-list-col-right > div > div > div.puisg-row > div > div > div > div:last-child > div > a > div > span:last-child > span::text").get()
            # Current Rating - PRIMARY ORDERING CRITERIA
            item["rating"] = product.css("div.puis-list-col-right > div > div > div[data-cy=reviews-block] > div > span > a::attr(aria-label)").get()[:3]
            # Current Number of Reviews - TERTIARY ORDERING CRITERIA
            item["review_count"] = product.css("div.puis-list-col-right > div > div > div[data-cy=reviews-block] > div > span:last-child > div > a > span::text").get()
            yield item

        next_page = response.css("a.s-pagination-next::attr(href)").get()
        if next_page is not None:
           yield response.follow(next_page, self.parse)