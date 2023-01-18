from scrapy import Item, Field


class ChessScraperItem(Item):
    event = Field()
    site = Field()
    date = Field()
    event_date = Field()
    round = Field()
    result = Field()
    white_player = Field()
    black_player = Field()
    opening = Field()
    white_elo = Field()
    black_elo = Field()
    ply_count = Field()
    moves = Field()
    ratio = Field()


class ChessLinkItem(Item):
    link = Field()
