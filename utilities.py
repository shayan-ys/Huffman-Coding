import json


def read_json_file(filename: str) -> dict:
    with open(filename) as json_data:
        return json.load(json_data)


def read_file(filename: str) -> bytes:
    input_file = open(filename, 'rb')
    return input_file.read()


def read_text_file(filename: str) -> str:
    input_file = open(filename, 'r')
    return input_file.read()
