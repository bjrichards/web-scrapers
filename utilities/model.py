from typing import TypedDict


class Export_Data(TypedDict):
    filename: str | None
    target_dir: str | None
    data: list[dict]
