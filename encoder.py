from utilities import read_file
from collections import Counter
import json


def count_characters(text: bytes) -> Counter:
    text_list = [char for char in text]
    return Counter(text_list)


def write_text_file(filename: str, output: iter, char_mapping: dict=None):
    if char_mapping:
        mapped_str = ''
        for char in output:
            mapped_str += char_mapping[char]
        output = mapped_str

    with open(filename, 'w') as outfile:
        outfile.write(output)


def write_json_file(filename: str, output: dict):
    with open(filename, 'w') as outfile:
        json.dump(output, outfile)


def make_nodes_list_and_orphan_counter(char_counter: Counter) -> (list, Counter):
    inner_nodes_list = []
    inner_orphan_dict = {}
    index = 0
    for char, count in char_counter.items():
        inner_nodes_list.append(char)
        inner_orphan_dict[index] = count
        index += 1

    return inner_nodes_list, Counter(inner_orphan_dict)


def make_tree(node_index: int, nodes_list: list, char_mapping: dict={}, traverse_str: str='') -> (dict, dict):
    node = nodes_list[node_index]
    if isinstance(node, int):
        char_mapping[node] = traverse_str
        return node, char_mapping
    else:
        left, char_mapping = make_tree(node[0], nodes_list, char_mapping, traverse_str + '0')
        right, char_mapping = make_tree(node[1], nodes_list, char_mapping, traverse_str + '1')
        return {0: left, 1: right}, char_mapping


def encode(filename: str):
    input_bytes = read_file(filename)
    characters_counter = count_characters(input_bytes)
    print(characters_counter)

    nodes_list, orphan_counter = make_nodes_list_and_orphan_counter(characters_counter)
    print(nodes_list)
    print(orphan_counter)

    print(characters_counter.most_common()[-2:])
    print(len(characters_counter))

    while len(orphan_counter) >= 2:
        selected_nodes = orphan_counter.most_common()[-2:]
        left = selected_nodes[0]  # tuple (key: value)
        right = selected_nodes[1]
        # new_node = {0: nodes_list[left[0]], 1: nodes_list[right[0]]}
        new_node = (left[0], right[0])
        new_node_value = left[1] + right[1]
        new_node_index = len(nodes_list)

        del orphan_counter[left[0]]
        del orphan_counter[right[0]]
        orphan_counter[new_node_index] = new_node_value

        nodes_list.append(new_node)

    print(orphan_counter)
    root_node_index = orphan_counter.most_common()[0][0]
    print(nodes_list)
    print(nodes_list[root_node_index])

    tree, char_mapping = make_tree(root_node_index, nodes_list)

    print(tree)
    print(char_mapping)

    write_json_file('manifest.json', tree)
    write_text_file('compressed.bin', input_bytes, char_mapping)


# test_text = "mississippi river"
# test_text = read_file('sample.txt')
#
encode('sample.png')

# with open("sample.txt", "rb") as imageFile:
#     f = imageFile.read()
#
# b_int = list(map(int, f))
# print(b_int[:10])

# with open("sample2.png", "wb") as imageFile:
#     imageFile.write(bytearray(b_int))
