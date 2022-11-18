import scrapy
from chess_games_spider.items import ChessGamesItem
from itemloaders import ItemLoader


class ChessGamesSpider(scrapy.Spider):
    name = "GamesSpider"

    def start_requests(self):
        urls = [
            'https://www.chessgames.com/perl/chess.pl?page=1&pid=14380',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        # get href of next page to access another set of games
        next_page = response.xpath("//td[@background='/chessimages/table_stripes.gif']"
                                   "/a/img[@src='/chessimages/next.gif']/parent::*/@href").get()

        # get href of games in white and brown background
        game_pages = response.xpath("//*/tr[@bgcolor='#FFFFFF']/td/font/a/@href").extract()
        game_pages.extend(response.xpath('//*/tr[@bgcolor="#EEDDCC"]/td/font/a/@href').getall())

        game_pages = [response.urljoin(game_page) for game_page in game_pages]

        # yield {'GAMES': game_pages}
        # yield {'NEXT PAGE': next_page}

        # for each game in games_pages list yield parse_game with its url
        for games_page in game_pages:
            yield scrapy.Request(url=games_page, callback=self.parse_game)

        # if there is next page yield parse of it
        # if next_page:
        #     next_page = response.urljoin(next_page)
        #     yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_game(self, response):
        game_info = ItemLoader(selector=ChessGamesItem)

        # get date, place, opening and outcome
        data = response.xpath("//font[@face='georgia,palatino,times new roman,times']/text()").getall()

        # data[3] = data[3].replace('\xa0 ', '').replace('\n    ', '')
        # data[0] = data[0].replace('\n    ', '')
        # data[1] = data[1].replace('\n    ', '').replace(' ', '')

        game_info.add_value('players', response.xpath("//div/font[@face='verdana,arial,helvetica']/b/a/text()").getall())
        # we pass uncleared data to outcome, place_date and opening Fields
        game_info.add_value('outcome', data[3])
        game_info.add_value('place_date', data[0])
        game_info.add_value('opening', data[1])
        # data is placed on javascript
        game_info.add_value('moves', response.xpath("//div[@id='score_box']/button/text()").getall())

        yield game_info.load_item()

       
