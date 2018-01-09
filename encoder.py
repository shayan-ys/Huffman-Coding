from utilities import write_json_file, write_compressed_bin_file, read_bin_file
import defaults

from collections import Counter
import sys


def count_characters(text: bytes) -> Counter:
    text_list = [char for char in text]
    return Counter(text_list)


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
    input_bytes = read_bin_file(filename)
    characters_counter = count_characters(input_bytes)

    nodes_list, orphan_counter = make_nodes_list_and_orphan_counter(characters_counter)

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

    root_node_index = orphan_counter.most_common()[0][0]

    tree, char_mapping = make_tree(root_node_index, nodes_list)

    write_json_file(defaults.manifest_file_prefix + filename + defaults.manifest_file_extension, tree)
    write_compressed_bin_file(filename + defaults.compressed_file_extension, input_bytes, char_mapping)


filename = 'sample.txt'
if sys.argv and len(sys.argv) > 1:
    filename = sys.argv[1]

encode(filename)
print("Compression process finished.")
