# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MCItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field() # Direct Product URL
    name = scrapy.Field() # Product Name as Listed
    current_price = scrapy.Field() # Current Price/Regular Price if not on sale
    regular_price = scrapy.Field() # Regular Price if on sale, returns None if not on sale
    stock = scrapy.Field() # Current inventory count (Scraper is only looking for in stock items right now)

class AMZItem(scrapy.Item):
    url = scrapy.Field() # Direct Product URL
    name = scrapy.Field() # Product Name as Listed
    current_price = scrapy.Field() # Current Price/Regular Price if not on sale
    regular_price = scrapy.Field() # Regular Price if on sale, returns None if not on sale
    rating = scrapy.Field() # Product Rating
    review_count = scrapy.Field() # Number of Reviews