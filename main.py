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
    :return: Two lists with ID and Parent_IDs respectively
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
    Creates a tree structure by first hashing all node's ids into hashmap.
    Then find every parent id and add as child. Use hashmaps constant look up time O(1) to our advantage.
    :param root: Root of the tree to be created
    :param node_list: List of nodes that have both a own unique ID and a Parent_ID.
    :return: Root of created tree.
    """
    hashmap = {root.id: root}

    for node in node_list:
        hashmap[node.id] = node

    for node in node_list:
        hashmap[node.parent_id].add_child(hashmap[node.id])

    create_depth([root])
    return root


def create_depth(node_list: List[Node], depth=1):
    """
    Go through tree recursively and increment depth counter for each level
    :param node_list: list of root nodes
    :param depth: start depth
    :return: None. Mutate roots in node_list
    """
    for node in node_list:
        node.depth = depth
        create_depth(node.children, depth + 1)


def find_maximum(root: Node, max_depth=1) -> int:
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


def find_nodes_at_depth(root: Node, depth: int, current_nodes: List[Node] = []) -> List[Node]:
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


def find_path(root: Node, start_node: Node, end_node: Node) -> List[Node]:
    """
    Find path from start_node to end_node.
    Find parent path from both start node and end node and then find first common node in both paths
    Remove excess nodes from both paths and concat them to a combined path.
    Reverse path_two such that the final path is in sorted order.
    :param root: Root node of a given tree
    :param start_node: node we want to find path from
    :param end_node: node we want to find path to
    :return: path of nodes or empty path if there is no such path.
    """
    current_node = start_node
    path_one = []
    while current_node != root:
        path_one.append(current_node)
        current_node = current_node.parent
        if current_node == end_node:
            path_one.append(current_node)
            return path_one

    current_node = end_node
    path_two = []
    while current_node != root:
        path_two.append(current_node)
        current_node = current_node.parent
        if current_node == start_node:
            path_two.append(current_node)
            path_two.reverse()
            return path_two

    common_node = None
    for node in path_one:
        if node in path_two:
            common_node = node
            break
    if common_node is None:
        return []

    path_one = path_one[0: path_one.index(common_node)+1]
    path_two = path_two[0: path_two.index(common_node)]
    path_two.reverse()
    final_path = path_one + path_two
    return final_path


def find_route(root: Node, start_id: int,  end_id: int) -> List[Node]:
    """
    Find route from a node with a id = start_id to another node with id = end_id
    :param root: root of the tree we want to search in
    :param start_id: id of the node we want to search from
    :param end_id: id of the node we want to find
    :return: List of Nodes encountered in the path from start to end.
    """
    start_node = find_node(root, start_id)
    end_node = find_node(root, end_id)
    route = find_path(root, start_node, end_node)
    if route.__len__() == 0:
        return []
    return route


def main() -> None:
    id_list, parent_id_list = read_file('Oppgave.xlsx')
    root, node_list = create_node_list(id_list, parent_id_list)
    create_tree(root, node_list)
    start_program(root)


def start_program(root: Node) -> None:
    while True:
        print("+------------------------Demo of methods---+---------------+")
        print("| Check how many levels there are?         | Press 0       |")
        print("| Check which IDs are at a level?          | Press 1       |")
        print("| Check the path from one Node to another? | Press 2       |")
        print("| To exit                                  | Press 3       |")
        print("+------------------------------------------+---------------+")
        answer = input("Choose an action: ")
        if answer == '0':
            print(f'There are: {find_maximum(root)} levels to this tree with root {root}')
        if answer == '1':
            level_number = int(input("Choose a level: "))
            pprint(find_nodes_at_depth(root, level_number))
        if answer == '2':
            start_id = int(input("Start id: "))
            end_id = int(input("End id: "))
            pprint(find_route(root, start_id, end_id))
        if answer == '3':
            break


if __name__ == '__main__':
    main()
