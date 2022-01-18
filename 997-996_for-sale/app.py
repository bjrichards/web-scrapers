import random
import time
from dataclasses import dataclass
from typing import Optional

import bs4  # type: ignore
import requests  # type: ignore
import xlsxwriter  # type: ignore


# car dataclass
@dataclass
class car:
    vin: str = ""
    stock_num: Optional[str] = ""
    year: Optional[str] = ""
    title: Optional[str] = ""
    price: Optional[str] = ""
    mileage: Optional[str] = ""
    drivetrain: Optional[str] = ""
    sale_link: Optional[str] = ""

    def __str__(self):
        return (f'\tVIN: {self.vin} \n\
        Stock Number: {self.stock_num} \n\
        Year: {self.year} \n\
        Title: {self.title} \n\
        Price: {self.price} \n\
        Mileage: {self.mileage} \n\
        Drivetrain: {self.drivetrain} \n\
        Sales Link: {self.sale_link}'
        )
# Cars.com
class scraper_cars_dot_com():
    prefix: str = "https://www.cars.com/shopping/results/?"
    link_prefix: str = "https://www.cars.com"
    tags: list[str] = [
        "maximum_distance=250",             # max mileage away (250 miles)
        "makes[]=porsche",                  # make of Porsche
        "models[]=porsche-911",             # model of 911
        "transmission_slugs[]=manual",      # manual transmission
        "page_size=100",                    # page size of 100
        "sort=best_match_desc",             # needed sort choice for website
        "stock_type=used",                  # used cars only
        "zip=89519"                         # zip code of area I want to shop around
    ]

    soup: bs4.BeautifulSoup
    links: list = []
    cars: list[car] = []

    def __init__(self) -> None:
        pass

    def run(self) -> None:
        self.retrieve_site()
        self.grab_links()
        self.get_each_car_info()

    def retrieve_site(self) -> None:
        url = self.compile_url()
        page = requests.get(url)
        self.soup = bs4.BeautifulSoup(page.content, "html.parser")

    def grab_links(self) -> None:
        for link in self.soup.find_all("a", {"class":"vehicle-card-link"}, href=True):
            if link.text:
                self.links.append(link['href'])

    def get_each_car_info(self) -> None:
        for link in self.links:
            car_link = self.link_prefix + link
            car_info = self.get_car_info(car_link)
            if car_info:
                self.cars.append(car_info)
            time.sleep(random.randint(0,3))

    def get_car_info(self, car_link) -> Optional[car]:
        result: car = car()
        cleaned_id_text: list[str] = []
        cleaned_id_attribute_text: list[str] = []

        car_page = requests.get(car_link)
        soup = bs4.BeautifulSoup(car_page.content, "html.parser")

        # Get drivetrain, vin, stock #, and mileage
        info_group = soup.find_all("dl", {"class":"fancy-description-list"}) 
        for i in info_group[0].find_all("dt"):
            cleaned_id_text.append(i.text)

        for i in info_group[0].find_all("dd"):
            cleaned_id_attribute_text.append(i.text)

        for i in range(0, len(cleaned_id_text)):
            id: str = cleaned_id_text[i]
            data: str = cleaned_id_attribute_text[i]
            if id == "Drivetrain":
                result.drivetrain = data
            elif id == "VIN":
                result.vin = data
            elif id == "Stock #":
                result.stock_num = data
            elif id == "Mileage":
                result.mileage = data.replace(".", "")

        # Get price
        price = soup.find("span", {"class":"primary-price"}).text # type: ignore
        result.price = price

        # Get title
        title = soup.find("h1", {"class":"listing-title"}).text # type: ignore
        result.title = title

        # Set sales link
        result.sale_link = car_link

        # Get Year
        result.year = title[0:5]

        if result.vin:
            return result
        else:
            return None

    def compile_url(self) -> str:
        result: str = ""

        result += self.prefix

        for tag in self.tags:
            result += tag
            result += "&"
        
        # remove hangin '&' on end
        result = result[:-1]

        return result


class excel_controller():
    workbook_name: str = "911_for_sale.xlsx"

    def add_data_to_workbook(self, data: list[car]):
        workbook = xlsxwriter.Workbook(self.workbook_name)
        worksheet = workbook.add_worksheet()

        row = 0
        col = 0

        for car in data:
            worksheet.write(row, col, car.vin)
            worksheet.write(row, col+1, car.year)
            worksheet.write(row, col+2, car.title)
            worksheet.write(row, col+3, car.price)
            worksheet.write(row, col+4, car.mileage)
            worksheet.write(row, col+5, car.drivetrain)
            worksheet.write(row, col+6, car.stock_num)
            worksheet.write(row, col+7, car.sale_link)

            row +=1
        workbook.close()

if __name__ == "__main__":
    cars_com: scraper_cars_dot_com = scraper_cars_dot_com()
    excel_contr: excel_controller = excel_controller()
    
    cars_com.run()
    excel_contr.add_data_to_workbook(cars_com.cars)

