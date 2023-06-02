import dataclasses
from typing import Optional


@dataclasses.dataclass
class business_info:
    name: str
    address: str
    city: str
    state: str
    zipcode: str

    business_category: str
    bio: str
    last_updated: str

    estimated_employees: int | None = None

    email: str | None = None
    phone_number: str | None = None
    website: str | None = None
    contact_name: str | None = None

    services: str | None = None
    major_clients: str | None = None
    affiliations: str | None = None


@dataclasses.dataclass
class scraping_url_info:
    name: str
    url: str
