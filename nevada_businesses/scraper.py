from typing import Tuple

import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from model import business_info


def scrape_data_worker(url: str) -> business_info:
    soup = get_soup(url)
    details_grouping = get_details_grouping(soup)
    title = get_business_name(soup)
    last_updated_time = get_entry_time(soup)

    data: dict = {}
    for item in details_grouping.find_all("div", {"class", "wpbdp-field-display"}):  # type: ignore
        label, value = get_label_value_pair(item)
        data[label] = value

    return massage_data_into_business_info_format(
        data, name=title, last_updated=last_updated_time
    )


def get_soup(url: str) -> BeautifulSoup:
    page = requests.get(url)
    result = BeautifulSoup(page.content, "html.parser")
    return result


def get_business_name(soup: BeautifulSoup) -> str:
    return soup.find("a", {"class", "main-title"}).text  # type:ignore


def get_entry_time(soup: BeautifulSoup) -> str:
    return soup.find("time", {"class", "entry-time"}).text  # type:ignore


def get_details_grouping(soup: BeautifulSoup) -> NavigableString | Tag | None:
    result = soup.find("div", {"class", "listing-details"})
    return result


def get_label_value_pair(tag: Tag) -> Tuple[str, str]:
    result_label: str = ""
    result_value: str = ""

    result_label = tag.find("span", {"class", "field-label"}).text  # type:ignore
    result_value = tag.find("div", {"class", "value"}).text  # type:ignore

    return result_label, result_value


def massage_data_into_business_info_format(
    data: dict, name: str, last_updated: str
) -> business_info:
    result = business_info(
        name=name,
        address=data["*Address"],
        city=data["*City"],
        state=data["*State"],
        zipcode=data["*Zipcode"],
        business_category=data["Business Genre"],
        bio=data["*Company Bio"],
        last_updated=last_updated,
        estimated_employees=data.get("Number of Employees in Nevada"),
        email=data.get("Contact Email"),
        phone_number=data.get("Phone"),
        website=data.get("Website"),
        contact_name=data.get("Contact Name, Title"),
        services=data.get("Specialties, Products, Brands, Services Offered"),
        major_clients=data.get("Major Clients"),
        affiliations=data.get("Professional Affiliations, Associations & Memberships"),
    )
    return result


if __name__ == "__main__":
    url = "https://nevadabusiness.com/nbm-business-directory/38271/eugene-burger-management-corporation-4/"
    print(scrape_data_worker(url))
