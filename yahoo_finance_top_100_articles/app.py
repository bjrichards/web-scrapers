# Written by Braeden Richards
# Created on May 30, 2023
# Contact: braedae.software@gmail.com
#
# Last updated on May 30, 2023
#
# Copyright (c) 2023 - Braeden Richards, All rights reserved.

import csv  # For writing dataclass to csv
import dataclasses
import time  # For sleep function

from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# To ensure chrome driver is always available to application
from webdriver_manager.chrome import ChromeDriverManager

config: dict = {
    "csv": {"filename": "yahoo_finance_articles.csv", "output_dir": "."},
    "target_url": "https://finance.yahoo.com/news",
    "target_number_of_articles": 100,
    "page_scroll_sleep_time": 2,
}


@dataclasses.dataclass
class yahoo_article_info:
    """Contains all required information of Yahoo Finance Article for export.

    Fields:
        title: Title of article.
        link: Link to source of article.
        source: Originating author source of article (Forbes, Yahoo Finance, Bloomsberg, etc.).
        age_at_pull: How long the article has been out at time of web scrape.
        category: Category of article (Business, Finance, World, etc.).
        description: Short example/description provided for article.
    """

    title: str
    link: str
    source: str
    age_at_pull: str
    category: str
    description: str


def get_article_data(src: Tag) -> yahoo_article_info:
    """Given BS4 Tag containing article information, parse and grab article info and return yahoo_article_info dataclass of information."""
    header = src.find("h3")
    title = header.find("a").text  # type: ignore
    href = header.find("a")["href"]  # type: ignore
    link = config["target_url"] + href  # type: ignore

    spans = src.find_all("span")
    source = spans[0].text
    age_at_pull = spans[1].text

    category = src.find("div", {"data-test-locator": "catlabel"}).text  # type: ignore

    description = src.find("p").text  # type: ignore

    result = yahoo_article_info(
        title=title,
        link=link,
        source=source,
        age_at_pull=age_at_pull,
        category=category,
        description=description,
    )
    return result


# Selenium driver to open browser
driver = webdriver.Chrome(ChromeDriverManager().install())

# Navigate open browser to target url
driver.get(config["target_url"])

# Since Yahoo Finance uses scroll based loading instead of pages, scroll to
#   bottom of page and wait 2 seconds. Repeat 10 times to ensure enough
#   articles are loaded for scraper to grab target number of articles.
for _ in range(10):
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.END)
    time.sleep(config["page_scroll_sleep_time"])

# Obtain raw html, convert to BS4 format, grab main body of information.
html: str = driver.page_source
soup = BeautifulSoup(html, "html.parser")
main_soup = soup.find("div", {"id": "Main"})

# Obtain each article from loaded page as a Tag object
articles: list = []
if main_soup and type(main_soup) == Tag:
    articles = main_soup.find_all("li", {"class": "js-stream-content"})
print(f"{len(articles)} articles obtained. Starting parsing of each article.")

# Parse each Tag object into yahoo_article_info dataclasses until there are
#   target number of articles grabbed.
article_info_list: list[yahoo_article_info] = []
i: int = 0
while len(article_info_list) < 100 or i < len(articles):
    print(f"Article number: {i + 1}. {len(article_info_list)} in info list.")
    try:
        article_info_list.append(get_article_data(articles[i]))
    except:
        pass
    i += 1

print("Outputting to csv.")
# Output required information to csv.
with open(config["csv"]["filename"], "w", newline="") as f:
    fields = [field.name for field in dataclasses.fields(yahoo_article_info)]
    w = csv.DictWriter(f, fields)
    w.writeheader()
    w.writerows([info.__dict__ for info in article_info_list])
