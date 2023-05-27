# Chess Games Webscraping

This project aims to prototype a web scraping solution for extracting chess games from www.chessgames.com. The code provided serves as a basic foundation that can be deployed on a server or modified to suit your specific needs, such as saving the scraped data to a local database. The ultimate goal of this project is to build a comprehensive database of chess games.

## `chess_spider` Spider
The `chess_spider` is designed to scrape all chess games associated with a specific player. By replacing the current link (Mihail Tal) with any other player's link, the spider will yield all the games available for that player.

## `first_spider` Spider
The `first_spider` is responsible for initially scraping every player's link from chessgames.com. It then proceeds to scrape each player's games one by one, systematically gathering the data.

## `final_spider` Spider
The `final_spider` operates similarly to the `first_spider`, but with a difference. It utilizes pre-stored data of all players' links in a text file. Subsequently, it proceeds to scrape the games of each specific player individually.

##
By utilizing the provided spiders, you can scrape and extract chess games from www.chessgames.com. These spiders serve as a starting point for building a comprehensive database of chess games, which can be further enhanced and customized to suit your specific requirements.

