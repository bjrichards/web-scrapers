from crawler import crawler
from export import export_to_csv
from model import business_info
from scraper import scrape_data_worker

if __name__ == "__main__":
    starting_url: str = (
        "https://nevadabusiness.com/nbm-business-directory/?wpbdp_view=all_listings"
    )
    site_crawler: crawler = crawler(start_url=starting_url, crawl_max_speed=10)

    site_crawler.crawl()
    print(f"Number of site_crawler grabbed pages: {len(site_crawler._url_list)}")

    data: list = [business_info]
    for i in range(0, 10):
        data.append(scrape_data_worker(site_crawler._url_list[i].url))
    # data.append(
    #     scrape_data_worker(
    #         "https://nevadabusiness.com/nbm-business-directory/38271/eugene-burger-management-corporation-4/"
    #     )
    # )

    export_to_csv(filename="data.csv", data=data)
