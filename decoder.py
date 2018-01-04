from utilities import read_file, read_json_file

compressed_bits = read_file('compressed.bin')
tree = read_json_file('manifest.json')

orig_text = ''
node = tree
for char in compressed_bits:
    node = node[char]
    if isinstance(node, str):
        orig_text += node
        node = tree

print(orig_text)
