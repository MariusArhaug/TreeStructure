import pandas as pd
import math
from node import Node


def read_file(file):
    data = pd.read_excel(rf'{file}', sheet_name="Data", usecols=['ID', 'PARENT_ID'])
    id_list = data['ID'].tolist()
    parent_list = data['PARENT_ID'].tolist()
    return id_list, parent_list


def write_to_file(root, filename):
    with open (filename, 'w') as file:
        output = root.to_JSON()
        file.write(output)


def create_node_list():
    id_list, parent_list = read_file('Oppgave.xlsx')

    nodes = []
    root_node = None
    for id, parent_id in zip(id_list, parent_list):
        if math.isnan(parent_id):
            root_node = Node(id, None)
            continue
        nodes.append(Node(id, int(parent_id)))
    nodes = sorted(nodes, key=lambda x: x.parent_id)

    return root_node, nodes

def create_tree(root, node_list):
    hashmap = {root.id: root}

    for node in node_list:
        hashmap[node.id] = node

    for node in node_list:
        hashmap[node.parent_id].add_child(hashmap[node.id])

    return root


def find_path(root, start_id, end_id):
    start_node = find_node(root, start_id)
    end_node = find_node(root, end_id)
    path = [start_node]
    relative_path = find_way(start_node, end_id)

    if end_node not in relative_path:
        relative_path = find_path(root, start_id, end_id)

    for node in relative_path:
        path.append(node)
    path.append(end_node)
    return path


def find_way(start_node, end_id, path=[]):
    for child in start_node:
        if child.id != end_id:
            path.append(child)
            if len(child.children) == 0:
                path = find_way(start_node, end_id, [])
            path = find_way(child, end_id, path)
    return path


"""def find_node(root, node_id):
    if root.id == node_id:
        return root
    for child in root:
        if child.id == node_id:
            return child
    for child in root:
        node = find_node(child, node_id)
        if node is not None:
            return node
    return None
"""


def find_node(root, node_id, path=[]):
    if len(path) == 0:
        path.append(root)

    if root.id == node_id:
        return path
    for child in root:
        if child not in path:
            path.append(child)
        new_path = find_node(child, node_id, path)

        if len(new_path) != 0:
            return new_path

    return []

"""
def find_maximum(graph, max_depth=1):
    
    Find deepest depth of element
    :param graph:
    :param max_depth:
    :return:
    
    new_max = max_depth
    for child in graph:
        if new_max < child.depth and len(child.children) == 0:
            new_max = child.depth
            continue
        return find_maximum(child.children, new_max)
    return new_max
"""

def find_maximum():
    pass


def find_biggest_depth_node(nodes, current_node=None):
    for node in nodes:
        if not current_node:
            current_node = node
        if current_node.depth < node.depth:
            current_node = node
        for child in node.children:
            return find_biggest_depth_node(node.children, current_node)
    return current_node


def find_nodes_at_depth(root, depth, current_nodes=[]):
    """
    Find all nodes at a given depth
    :param root: root of tree to search in
    :param depth: depth value
    :param current_nodes: list of observed nodes
    :return: list of nodes at given depth level
    """
    if root.depth == depth and root not in current_nodes:
        current_nodes.append(root)
    elif root.depth < depth:
        for child in root:
            current_nodes = find_nodes_at_depth(child, depth, current_nodes)
    return current_nodes


def create_hierarchy():
    root, node_list = create_node_list()
    root = create_tree(root, node_list)
    create_depth([root])
    # write_to_file(root, 'print1.txt')
    # print(root.to_JSON())
    # print(find_maximum(root))
    # path = find_node(root, 28792)
    # for node in path:
    #    print(node)
    # print(find_biggest_depth_node([root]))
    # print(find_nodes_at_depth([root], find_maximum(root)))
    # print(find_nodes_at_depth(root, 4))


def create_depth(node_list, depth=1):
    """
    Go through tree recursively and increment depth counter for each level
    :param node_list: list of root nodes
    :param depth: start depth
    :return: None. Mutate roots in node_list
    """
    for node in node_list:
        node.depth = depth
        create_depth(node.children, depth + 1)


if __name__ == '__main__':
    create_hierarchy()
