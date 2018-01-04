from utilities import read_text_file, read_json_file

compressed_bits = read_text_file('compressed.bin')
tree = read_json_file('manifest.json')

orig_bytes = []
node = tree
for char in compressed_bits:
    node = node[char]
    if isinstance(node, int):
        orig_bytes.append(node)
        node = tree


with open("sample_decoded.png", "wb") as imageFile:
    imageFile.write(bytearray(orig_bytes))
