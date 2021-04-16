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

    def add_child(self, node):
        """
        Add child to node if this node is parent of incoming node
        :param node: child to be added
        :return: None
        """
        if self.is_parent(node):
            self.children.append(node)

    def is_parent(self, node):
        return self.id == node.parent_id

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)

    def __repr__(self):
        return f"ID: {self.id} ParentID: {self.parent_id} Depth: {self.depth}"

    def __iter__(self):
        return iter(self.children)

    def walk(self):
        """
        walk through nodes in node
        :return:
        """
        yield self
        for child in self:
            yield from child.walk()

