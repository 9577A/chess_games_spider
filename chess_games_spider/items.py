# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ChessGamesItem(scrapy.Item):
    players = scrapy.Field()
    # outcome = scrapy.Field()
    # place_date = scrapy.Field()
    # opening = scrapy.Field()
    additional_data = scrapy.Field()
    moves = scrapy.Field()
