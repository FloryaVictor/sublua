from ast import And
from .ast import *

import graphviz


def dfs(node: Node):
    id = 1
    node.parent = None
    def dfs_rec(node: Node):
        nonlocal id
        node.id = id
        id += 1
        for child in node.children():
            child.parent = node
            dfs_rec(child)
    dfs_rec(node)


def toGraphviz(node: Node, merge=True) -> graphviz.Digraph:
    dfs(node)
    graph = graphviz.Digraph()
    queue = [node]
    merge_envelope = {OrExpr, AndExpr}
    merge_ops = {EqExpr, CmpExpr, AddExpr, MulExpr, UnaryExpr}

    if merge:
        while queue:
            node = queue.pop(0)
            graph.node(str(node.id), str(node))
            for child in node.children():
                while (child.__class__ in merge_ops and len(child.ops) == 0) or (child.__class__ in merge_envelope and len(child.children()) == 1):
                    child = child.children()[0]
                queue.append(child)
                graph.edge(str(node.id), str(child.id))
    else:
        while queue:
            node = queue.pop(0)
            graph.node(str(node.id), str(node))
            for child in node.children():
                queue.append(child)
                graph.edge(str(node.id), str(child.id))
    return graph