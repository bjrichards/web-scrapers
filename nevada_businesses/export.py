import csv
import dataclasses

from model import business_info


def export_to_csv(filename: str, data: list[business_info]):
    print(dataclasses.asdict(data[0]))
    with open(filename, "w", newline="") as f:
        fields = [field.name for field in dataclasses.fields(business_info)]
        w = csv.DictWriter(f, fields)
        w.writeheader()
        w.writerows([dataclasses.asdict(info) for info in data])
