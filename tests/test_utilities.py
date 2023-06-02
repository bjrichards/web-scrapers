import dataclasses

import pytest

import utilities.csv_controller
import utilities.model


@pytest.fixture
def example_dataclass_def():
    """Definition of example dataclass."""

    @dataclasses.dataclass
    class Example_Dataclass:
        name: str
        title: str
        age: int
        height_inches: float

    return Example_Dataclass


@pytest.fixture
def example_dataclass(example_dataclass_def):
    """Example dataclass of exporting data."""
    result = example_dataclass_def("Braeden Richards", "Creator", 26, 69)
    return result


def test_csv_controller_export_dataclass(example_dataclass, example_dataclass_def):
    controller = utilities.csv_controller.CSV_Controller()

    filename = "test.csv"
    directory = "tests/test_exports"
    input_data = [example_dataclass]

    # Specified filename, directory. Correct data.
    # Expected: Correct
    data = utilities.model.Export_Data(
        filename=filename, target_dir=directory, data=input_data
    )
    result, message = controller.dump_from_dataclass(
        input_data=data, dataclass_type=example_dataclass_def
    )
    assert message == "Success" and result == True

    # No filename. Specified directory. Correct data.
    # Expected: Correct
    data["filename"] = None
    result, message = controller.dump_from_dataclass(
        input_data=data, dataclass_type=example_dataclass_def
    )
    assert message == "Success" and result == True

    # Specified filename, directory. No data in list.
    # Expected: Failure
    data["data"] = []
    result, message = controller.dump_from_dataclass(
        input_data=data, dataclass_type=example_dataclass_def
    )
    assert message == "No data in data list." and result == False
