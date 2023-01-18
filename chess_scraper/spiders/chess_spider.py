import scrapy
from scrapy import Request, Selector
import requests
from itemloaders import ItemLoader
from chess_scraper.items import ChessScraperItem, ChessLinkItem


class MySpider(scrapy.Spider):
    name = 'chess_spider'

    def start_requests(self):
        start_urls = [
            'https://www.chessgames.com/perl/chess.pl?page=1&pid=14380',
        ]
        for url in start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        # get href of next page to access another set of games
        next_page = response.xpath("//td[@background='/chessimages/table_stripes.gif']"
                                   "/a/img[@src='/chessimages/next.gif']/parent::*/@href").get()

        # get href of games in white and brown background
        game_pages = response.xpath("//*/tr[@bgcolor='#FFFFFF']/td/font/a/@href").extract()
        game_pages.extend(response.xpath('//*/tr[@bgcolor="#EEDDCC"]/td/font/a/@href').getall())

        game_pages = [response.urljoin(game_page) for game_page in game_pages]

        # yield Request(url=game_pages[9], callback=self.parse_game)
        # for each game in games_pages list yield parse_game with its url
        for game_page in game_pages:
            yield Request(url=game_page, callback=self.parse_game)

        # if next_page:
        #     yield Request(url=next_page, callback=self.parse)

    def parse_game(self, response):
        game_info = ItemLoader(selector=ChessScraperItem)
        url = response.urljoin('')
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'}
        # session = requests.Session()
        r = requests.get(url=url, headers=headers)

        sel = Selector(text=r.content)

        resp = sel.xpath('//div[@id="olga-data"]').getall()

        resp = resp[0]
        resp = resp[resp.index("pgn='"): resp.index("</div>")]

        #
        game_info.add_value("event", resp[resp.index('[Event "')+8: resp.index('"]\n[Site')])
        game_info.add_value("site", resp[resp.index('[Site "')+7: resp.index('"]\n[Date')])
        game_info.add_value("date", resp[resp.index('[Date "')+7: resp.index('"]\n[EventDate')])
        game_info.add_value("event_date", resp[resp.index('[EventDate "')+12: resp.index('"]\n[Round')])
        game_info.add_value("round", resp[resp.index('[Round "')+8: resp.index('"]\n[Result')])
        game_info.add_value("result", resp[resp.index('[Result "')+9: resp.index('"]\n[White')])
        game_info.add_value("white_player", resp[resp.index('[White "')+8: resp.index('"]\n[Black')])
        game_info.add_value("black_player", resp[resp.index('[Black "')+8: resp.index('"]\n[ECO')])
        game_info.add_value("opening", resp[resp.index('[ECO "')+6: resp.index('"]\n[WhiteElo')])
        game_info.add_value("white_elo", resp[resp.index('[WhiteElo "')+11: resp.index('"]\n[BlackElo')])
        game_info.add_value("black_elo", resp[resp.index('[BlackElo "')+11: resp.index('"]\n[PlyCount')])
        game_info.add_value("ply_count", resp[resp.index('[PlyCount "')+11: resp.index('"]\n\n')])
        game_info.add_value("moves", str(resp[resp.index('\n\n')+2: resp.index("' ratio")-4]).replace(' 1/2', ''))
        game_info.add_value("ratio", resp[resp.index("' ratio")+9: resp.index('" notes=')])

        yield game_info.load_item()


class FirstSpider(scrapy.Spider):
    name = 'first_spider'

    def start_requests(self):
        start_urls = [
            'https://www.chessgames.com/directory/', 'https://www.chessgames.com/directory/B',
            'https://www.chessgames.com/directory/C', 'https://www.chessgames.com/directory/D',
            'https://www.chessgames.com/directory/E', 'https://www.chessgames.com/directory/F',
            'https://www.chessgames.com/directory/G', 'https://www.chessgames.com/directory/H',
            'https://www.chessgames.com/directory/I', 'https://www.chessgames.com/directory/J',
            'https://www.chessgames.com/directory/K', 'https://www.chessgames.com/directory/L',
            'https://www.chessgames.com/directory/M', 'https://www.chessgames.com/directory/N',
            'https://www.chessgames.com/directory/O', 'https://www.chessgames.com/directory/P',
            'https://www.chessgames.com/directory/R', 'https://www.chessgames.com/directory/S',
            'https://www.chessgames.com/directory/T', 'https://www.chessgames.com/directory/U',
            'https://www.chessgames.com/directory/V', 'https://www.chessgames.com/directory/W',
            'https://www.chessgames.com/directory/X', 'https://www.chessgames.com/directory/Y',
            'https://www.chessgames.com/directory/Z',
        ]
        for url in start_urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        players_links = response.xpath("//center/table/tr/td/table/tr/td/table/tr/td/font/a/@href").extract()

        players_links = [response.urljoin(player_link) for player_link in players_links]

        for player_link in players_links:
            yield Request(url=player_link, callback=self.parse_player)

    def parse_player(self, response):
        # get href of next page to access another set of games
        next_page = response.xpath("//td[@background='/chessimages/table_stripes.gif']"
                                   "/a/img[@src='/chessimages/next.gif']/parent::*/@href").get()

        # get href of games in white and brown background
        game_pages = response.xpath("//*/tr[@bgcolor='#FFFFFF']/td/font/a/@href").extract()
        game_pages.extend(response.xpath('//*/tr[@bgcolor="#EEDDCC"]/td/font/a/@href').getall())

        game_pages = [response.urljoin(game_page) for game_page in game_pages]

        link = ItemLoader(selector=ChessLinkItem)

        for game_page in game_pages:
            link.add_value("link", game_page)

        yield link.load_item()

        if next_page:
            yield Request(url=next_page, callback=self.parse_player)


class FinalSpider(scrapy.Spider):
    name = 'final_spider'

    def start_requests(self):

        with open("out.txt", "r") as f:
            temp = f.read()
            data = temp.replace('\n', ' ').split()

        start_urls = data

        for url in start_urls:
            yield Request(url=url, callback=self.parse_game)

    def parse_game(self, response):
        game_info = ItemLoader(selector=ChessScraperItem)
        url = response.urljoin('')
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'}
        # session = requests.Session()
        r = requests.get(url=url, headers=headers)

        sel = Selector(text=r.content)

        resp = sel.xpath('//div[@id="olga-data"]').getall()

        resp = resp[0]
        resp = resp[resp.index("pgn='"): resp.index("</div>")]

        #
        game_info.add_value("event", resp[resp.index('[Event "') + 8: resp.index('"]\n[Site')])
        game_info.add_value("site", resp[resp.index('[Site "') + 7: resp.index('"]\n[Date')])
        game_info.add_value("date", resp[resp.index('[Date "') + 7: resp.index('"]\n[EventDate')])
        game_info.add_value("event_date", resp[resp.index('[EventDate "') + 12: resp.index('"]\n[Round')])
        game_info.add_value("round", resp[resp.index('[Round "') + 8: resp.index('"]\n[Result')])
        game_info.add_value("result", resp[resp.index('[Result "') + 9: resp.index('"]\n[White')])
        game_info.add_value("white_player", resp[resp.index('[White "') + 8: resp.index('"]\n[Black')])
        game_info.add_value("black_player", resp[resp.index('[Black "') + 8: resp.index('"]\n[ECO')])
        game_info.add_value("opening", resp[resp.index('[ECO "') + 6: resp.index('"]\n[WhiteElo')])
        game_info.add_value("white_elo", resp[resp.index('[WhiteElo "') + 11: resp.index('"]\n[BlackElo')])
        game_info.add_value("black_elo", resp[resp.index('[BlackElo "') + 11: resp.index('"]\n[PlyCount')])
        game_info.add_value("ply_count", resp[resp.index('[PlyCount "') + 11: resp.index('"]\n\n')])
        game_info.add_value("moves", str(resp[resp.index('\n\n') + 2: resp.index("' ratio") - 4]).replace(' 1/2', ''))
        game_info.add_value("ratio", resp[resp.index("' ratio") + 9: resp.index('" notes=')])

        yield game_info.load_item()
