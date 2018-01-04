import json


def read_json_file(filename: str) -> dict:
    with open(filename) as json_data:
        return json.load(json_data)


def read_file(filename: str) -> str:
    input_file = open(filename, 'r')
    return str(input_file.read())
