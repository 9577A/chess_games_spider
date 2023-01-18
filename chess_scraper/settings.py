BOT_NAME = 'chess_scraper'

SPIDER_MODULES = ['chess_scraper.spiders']
NEWSPIDER_MODULE = 'chess_scraper.spiders'
ROBOTSTXT_OBEY = True


TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
