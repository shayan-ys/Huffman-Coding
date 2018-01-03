from collections import Counter


def count_characters(text: str) -> Counter:
    text_list = [char for char in text]
    return Counter(text_list)


def read_file(filename: str) -> str:
    input_file = open(filename, 'r')
    return str(input_file.read())


def make_nodes_list_and_orphan_counter(char_counter: Counter) -> (list, Counter):
    inner_nodes_list = []
    inner_orphan_dict = {}
    index = 0
    for char, count in char_counter.items():
        inner_nodes_list.append(char)
        inner_orphan_dict[index] = count
        index += 1

    return inner_nodes_list, Counter(inner_orphan_dict)


def make_tree(node_index: int, traverse_str: str=''):
    node = nodes_list[node_index]
    if isinstance(node, str):
        char_mapping[node] = traverse_str
        return node
    else:
        left = make_tree(node[0], traverse_str + '0')
        right = make_tree(node[1], traverse_str + '1')
        return {0: left, 1: right}


test_text = "mississippi river"
# test_text = read_file('sample.txt')
characters_counter = count_characters(test_text)
print(characters_counter)

nodes_list, orphan_counter = make_nodes_list_and_orphan_counter(characters_counter)
print(nodes_list)
print(orphan_counter)

print(characters_counter.most_common()[-2:])
print(len(characters_counter))

while len(orphan_counter) >= 2:
    selected_nodes = orphan_counter.most_common()[-2:]
    left = selected_nodes[0]    # tuple (key: value)
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

char_mapping = {}
tree = make_tree(root_node_index)

print(tree)
print(char_mapping)
