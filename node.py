from __future__ import annotations
import json


class Node:
    def __init__(self, id, parent_id):
        """
        Init
        :param id: ID of node
        :param parent_id: ID of parent node
        """
        self.id = id
        self.parent_id = parent_id
        self.depth = 1
        self.children = []
        self.parent: Node

    def add_child(self, node: Node) -> None:
        """
        Add child to node if this node is parent of incoming node.
        Add parent to incoming child. Parent is "self"
        :param node: child to be added
        :return: None
        """
        if self.is_parent(node):
            self.children.append(node)
            node.add_parent(self)

    def is_parent(self, node: Node) -> bool:
        return self.id == node.parent_id

    def add_parent(self, node: Node) -> None:
        self.parent = node

    def to_JSON(self) -> str:
        return json.dumps(self.__to_dict__(), indent=2)

    def __repr__(self) -> str:
        return f"ID: {self.id} ParentID: {self.parent_id} Depth: {self.depth}"

    def __iter__(self) -> iter:
        return iter(self.children)

    def __to_dict__(self) -> dict:
        """
        Create a readable dictionary of object without circle reference errors
        Parent field is switched to toString method
        :return: dict of fields in Node object.
        """
        new_dict = {}
        for key, field in self.__dict__.items():
            if key == 'children':
                new_list = []
                for node in field:
                    new_list.append(node.__to_dict__())
                new_dict[key] = new_list
                continue
            if key == 'parent':
                continue
            new_dict[key] = field
        return new_dict

    def walk(self):
        """
        walk through nodes in node
        :return:
        """
        yield self
        for child in self:
            yield from child.walk()

