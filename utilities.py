import defaults
import json


def write_json_file(filename: str, output: dict):
    with open(filename, 'w') as outfile:
        json.dump(output, outfile)


def read_json_file(filename: str) -> dict:
    with open(filename) as json_data:
        return json.load(json_data)


def read_bin_file(filename: str) -> bytes:
    input_file = open(filename, 'rb')
    return input_file.read()


def read_text_file(filename: str) -> str:
    input_file = open(filename, 'r')
    return input_file.read()


def write_compressed_bin_file(filename: str, bitstring: iter, char_mapping: dict=None):

    if char_mapping:
        mapped_str = ''
        for char in bitstring:
            mapped_str += char_mapping[char]
        bitstring = mapped_str

    remaining_bits = ''
    input_int_list = [int(bitstring[i:i + defaults.chunk_size], 2) for i in range(0, len(bitstring), defaults.chunk_size)]
    if len(bitstring) % defaults.chunk_size:
        input_int_list = input_int_list[:-1]
        remaining_bits_count = len(bitstring) % defaults.chunk_size
        remaining_bits = [int(bit) + pow(2, defaults.chunk_size) for bit in bitstring[-remaining_bits_count:]]

    with open(filename, "wb") as openfile:
        openfile.write(bytearray(input_int_list + remaining_bits))


def read_compressed_bin_file(filename: str) -> str:
    with open(filename, "rb") as openfile:
        int_list = openfile.read()

    decoded_str = ''
    for byte in int_list:
        if byte < pow(2, defaults.chunk_size):
            decoded_str += '{0:0{width}b}'.format(byte, width=defaults.chunk_size)
        else:
            decoded_str += str(byte - pow(2, defaults.chunk_size))

    return decoded_str
