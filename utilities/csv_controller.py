import csv
import dataclasses
from typing import Tuple

from .model import Export_Data


class CSV_Controller:
    def __init__(self):
        self.default_filename = "data.csv"
        self.default_dir = "."

    def dump_from_dataclass(
        self,
        input_data: Export_Data,
        dataclass_type,
    ) -> Tuple[bool, str]:
        """
        Dumps all data from single or list of dataclasses into csv.

        Args:
            input_data: Structured dict containing all data, such as filename (if
                applicable), target directory (if applicable), and data to export.
            dataclass_type: Dataclass type definition. Used for obtaining column headers.

        Returns:
            True for success, False and error message for failure
        """
        if not input_data["data"]:
            return False, "No data in data list."

        filename, target_dir = self._get_targets(input_data)
        if not filename:
            filename = self.default_filename
        if not target_dir:
            target_dir = self.default_dir
        try:
            data = input_data["data"]
            with open(f"{target_dir}/{filename}", "w", newline="") as f:
                headers = [field.name for field in dataclasses.fields(dataclass_type)]
                w = csv.DictWriter(f=f, fieldnames=headers)
                w.writeheader()
                w.writerows([info.__dict__ for info in data])

            return True, "Success"

        except Exception as e:
            return False, str(e)

    def _get_targets(self, data: Export_Data) -> Tuple[str | None, str | None]:
        """Gets and returns filename and directory if specified.

        Args:
            input_data: Structured dict containing all data, such as filename (if
                applicable), target directory (if applicable), and data to export.

        Returns:
            Filename and directory location if specified, None if not.
        """
        return self.__get_filename(data), self.__get_target_directory(data)

    def __get_filename(self, data: Export_Data) -> str | None:
        """Gets and returns filename if specified."""
        return data.get("filename")

    def __get_target_directory(self, data: Export_Data) -> str | None:
        """Gets and returns directory if specified."""
        return data.get("target_dir")
