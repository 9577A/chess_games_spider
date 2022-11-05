import scrapy


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
        next_page = response.xpath('//td[@background="/chessimages/table_stripes.gif"]'
                                   '//img[@src="/chessimages/next.gif"]/parent::node()/@href').get()

        # get href of games in white and brown background
        games_pages = response.xpath('//').getall()
        games_pages.extend(response.xpath('//').getall())

        # for each game in games_pages list yield parse_game with its url
        for games_page in games_pages:
            yield scrapy.Request(url=games_page, callback=self.parse_game)

        # if there is next page yield parse of it
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse_game)

    def parse_game(self, response, **kwargs):
        pass
