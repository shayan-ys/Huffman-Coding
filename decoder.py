from utilities import read_compressed_bin_file, read_json_file
import defaults
import sys


def decode(filename: str):

    tree = read_json_file(defaults.manifest_file_prefix + filename + defaults.manifest_file_extension)
    compressed_bits = read_compressed_bin_file(filename + defaults.compressed_file_extension)

    orig_bytes = []
    node = tree
    for char in compressed_bits:
        node = node[char]
        if isinstance(node, int):
            orig_bytes.append(node)
            node = tree

    with open(defaults.decompressed_file_prefix + filename, "wb") as openfile:
        openfile.write(bytearray(orig_bytes))


filename = 'sample.txt'
if sys.argv and len(sys.argv) > 1:
    filename = sys.argv[1]

decode(filename)
print('Decompressed Successfully, check: "' + defaults.decompressed_file_prefix + filename + '"')
