import pandas as pd
import pprint
import json
import math


def read_file(file):
    data = pd.read_excel(rf'{file}', sheet_name="Data", usecols=['ID', 'PARENT_ID'])
    id_list = data['ID'].tolist()
    parent_list = data['PARENT_ID'].tolist()
    return id_list, parent_list


class Node:
    def __init__(self, id, parent_id):
        self.id = id
        self.parent_id = parent_id
        self.children = []

    def add_child(self, node):
        if self.is_parent(node):
            self.children.append(node)

    def is_parent(self, node):
        return self.id == node.parent_id

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def __repr__(self):
        return f"ID: {self.id} ParentID: {self.parent_id} {self.children}"


def create_hierarchy():
    root, node_list = create_node_list()
    graph = create_tree(root, node_list)
    print(graph.to_JSON())


def create_tree(root, node_list):
    hashmap = {root.id: root}

    for node in node_list:
        hashmap[node.id] = node

    for node in node_list:
        hashmap[node.parent_id].add_child(hashmap[node.id])

    return root


def create_node_list():
    id_list, parent_list = read_file('Oppgave.xlsx')

    nodes = []
    root_node = None
    for id, parent_id in zip(id_list, parent_list):
        if math.isnan(parent_id):
            root_node = Node(id, 'root')
            continue
        nodes.append(Node(id, int(parent_id)))
    # nodes = sorted(nodes, key=lambda x: x.parent_id)

    return root_node, nodes


if __name__ == '__main__':
    create_hierarchy()
