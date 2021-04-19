from __future__ import annotations
from node import Node
from typing import Optional, List, Tuple
import pandas as pd
import math
from pprint import pprint


def read_file(filename: str) -> Tuple[List[str], List[str]]:
    """
    Read file
    :param filename: Read file with filename
    :return: Two lists with ID and PArent_IDs respectively
    """
    data = pd.read_excel(rf'{filename}', sheet_name="Data", usecols=['ID', 'PARENT_ID'])
    id_list = data['ID'].tolist()
    parent_list = data['PARENT_ID'].tolist()
    return id_list, parent_list


def write_to_file(root: Node, filename: str) -> None:
    with open(filename, 'w') as file:
        output = root.to_JSON()
        file.write(output)


def create_node_list(id_list: List[str], parent_list: List[str]) -> Tuple[Node, List[Node]]:
    """
    Transform lists of ID and ParentID into Node objects with corresponding data
    Assumes theres only one root
    :param id_list: List of ID for nodes
    :param parent_list: List of ID for parent of nodes
    :return: Root and List of Nodes
    """
    nodes = []
    root_node = None
    for id, parent_id in zip(id_list, parent_list):
        if math.isnan(parent_id):
            root_node = Node(int(id), None)
            continue
        nodes.append(Node(int(id), int(parent_id)))
    return root_node, nodes


def create_tree(root: Node, node_list: List[Node]) -> Node:
    """

    :param root:
    :param node_list:
    :return:
    """
    hashmap = {root.id: root}

    for node in node_list:
        hashmap[node.id] = node

    for node in node_list:
        hashmap[node.parent_id].add_child(hashmap[node.id])

    create_depth([root])
    return root


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


def find_maximum(root: Node, max_depth: int = 1) -> int:
    """
    Find deepest depth level of leaf nodes in a given tree
    :param root: Root of tree
    :param max_depth: int value of the deepest level
    :return: max_depth: int
    """
    new_max = max_depth
    for child in root:
        if new_max < child.depth and len(child.children) == 0:
            new_max = child.depth
            continue
        new_max = find_maximum(child.children, new_max)
    return new_max


def find_node(root: Node, node_id: int) -> Optional[Node]:
    """
    Find node with a given node-id
    :param root: root of the tree we want to search for the node
    :param node_id: id of the node we want
    :return: Node if found, or None if the ID does not exist
    """
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


def find_nodes_at_depth(root: Node, depth: int, current_nodes: List[Node] = []):
    """
    Find all nodes at a given depth
    :param root: root of tree to search in
    :param depth: depth value
    :param current_nodes: list of observed nodes
    :return: list of nodes at given depth level, the list is sorted by the first visited node
    """
    if root.depth == depth and root not in current_nodes:
        current_nodes.append(root)
    elif root.depth < depth:
        for child in root:
            current_nodes = find_nodes_at_depth(child, depth, current_nodes)
    return current_nodes


def find_route_up(start_node: Node, end_id: int, path: List[Node] = []) -> List[Node]:
    """

    :param start_node:
    :param end_id:
    :param path:
    :return:
    """
    if start_node.parent_id is None and start_node.id != end_id:
        return []

    if start_node.id == end_id:
        path.append(start_node)
        return path

    path.append(start_node)
    return find_route_up(start_node.parent, end_id, path)


def find_route_down(start_node: Node, end_id: int, visited: List[Node] = [], path: List[Node] = []) -> List[Node]:
    """

    :param start_node:
    :param end_id:
    :param visited:
    :param path:
    :return:
    """
    for node in node_list:
        node.depth = depth
        create_depth(node.children, depth + 1)


if __name__ == '__main__':
    main()
