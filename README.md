# web-scrapers
Collection of web-scrapers of mine. There is no guarantee that a scraper can be grabbed and used directly without modification. With the nature of websites, there is always a possibility that a scraper is out of date and would need minor changes/updates to function fully.

These scrapers are simply meant to be used as templates, resources, or starting points for others. I created them for fun / some personal use and want to share them!

I have also created the [utilities](/utilities/) module to assist whomever with scraping. It includes simple nice to haves, such as a basic data format to store data to export and an exporting module to csv that works with dataclasses.

## Details

### Technologies Used (depending on scraper)
- Beautiful Soup (BS4)
- Selenium
- Requests

# Scrapers

## 996/996 Cars.com Scraper

[_997-996_for-sale_](/997-996_for-sale/)

Description: Scrapes [Cars.com](https://www.cars.com/) for 996/997 generation 911s, outputs car information (vin, year, model, trim, etc.) as well as location and price to an .xlsx.

## Nevada Business Scraper

[_nevada\_businesses_](/nevada_businesses/)

Description: Scrapes [nevadabusiness.com](https://nevadabusiness.com/nbm-business-directory/?wpbdp_view=all_listings) for all businesses. Scrapes business information (name, location, # of employees, contact email/number, etc.) and outputs to .csv.

## Yahoo Finance Scraper

[_yahoo\_finance\_top\_100\_articles_](/yahoo_finance_top_100_articles/)

Description: Scrapes [Yahoo Finance]() for top 100 articles. Scrapes link and article details (title, author, category, etc.). Outputs to a .csv.