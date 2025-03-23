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
            item["url"] = response.urljoin(product.css("div > div > div > span > div > div > div > div.puis-list-col-right > div > div > div > a::attr(href)").get())
            # Product Name as Listed
            item["name"] = product.css("div > div > div > span > div > div > div > div.puis-list-col-right > div > div > div > a > h2::attr(aria-label)").get()
            # Current Price/Regular Price if not on sale - SECONDARY ORDERING CRITERIA
            item["current_price"] = product.css("span.a-price > span::text").get()
            #item["current_price"] = product.css("div > div > div > span > div > div > div > div.puis-list-col-right > div > div > div.puisg-row > div > div > div > div:last-child > div > a > span > span::text").get()
            # Regular Price if on sale, returns None if not on sale
            item["regular_price"] = product.css("div.price > div.standardDiscount > strike::text").get()
            # Current Rating - PRIMARY ORDERING CRITERIA
            item["rating"] = product.css("div > div > div > span > div > div > div > div.puis-list-col-right > div > div > div[data-cy=reviews-block] > div > span > a::attr(aria-label)").get()[:3]
            # Current Number of Reviews - TERTIARY ORDERING CRITERIA
            item["review_count"] = product.css("div > div > div > span > div > div > div > div.puis-list-col-right > div > div > div[data-cy=reviews-block] > div > span:last-child > div > a > span::text").get()
            yield item

        next_page = response.css("ul.pages > li:last-child > a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


        # url = scrapy.Field() # Direct Product URL
        # name = scrapy.Field() # Product Name as Listed
        # current_price = scrapy.Field() # Current Price/Regular Price if not on sale
        # regular_price = scrapy.Field() # Regular Price if on sale, returns None if not on sale
        # rating = scrapy.Field() # Product Rating
        # review_count = scrapy.Field() # Number of Reviews
