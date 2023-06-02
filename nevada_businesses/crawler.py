import time

import requests
from bs4 import BeautifulSoup, Tag
from model import scraping_url_info


class crawler:
    def __init__(self, start_url, crawl_max_speed: int):
        self.start_url: str = start_url
        self.crawl_max_speed: int = crawl_max_speed

        self._url_list: list[scraping_url_info] = []

    def crawl(self) -> None:
        """Crawls through the site, grabs urls of businesses."""
        url = self.start_url
        while url:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            main_soup = soup.find("div", {"id", "wpbdp-page-all_listings"})
            if main_soup:
                self.__grab_business_urls_on_page(soup=main_soup)  # type: ignore
                url = self.__grab_next_page(main_soup)  # type: ignore
                time.sleep(self.crawl_max_speed)
            else:
                url = None

    def __grab_business_urls_on_page(self, soup: Tag) -> None:
        for listing in soup.find_all("div", {"id", "wpbdp-listing"}):
            link_info = listing.find("a")
            info = scraping_url_info(name=link_info.text, url=link_info["href"])
            print(f"Grabbing url number {len(self._url_list) + 1} | {info.url}")
            self.__add_link(link_info=info)

    def __grab_next_page(self, soup: Tag) -> str | None:
        next_grouping = soup.find("div", {"class", "wpbdp-pagination"})
        result: str | None = None
        try:
            if next_grouping:
                next = next_grouping.find("span", {"class", "next"})  # type: ignore
                result = next.find("a")["href"]  # type: ignore
                print("Going to next url.")
        except:
            print("No next button found")
        return result

    def __add_link(self, link_info: scraping_url_info) -> None:
        if link_info not in self._url_list:
            self._url_list.append(link_info)
