from operator import contains
from .ast import *
from .IR import *

import graphviz

from typing import List

from collections import defaultdict

class BasicBlock:
    def __init__(self) -> None:
        self.instructions = []
        self.edges = []
        self.id = -1

    def children(self) -> list:
        return self.edges

    def __str__(self) -> str:
        return "\n".join(map(str, self.instructions))


def buildCFG(code: List[Instruction]) -> List[BasicBlock]:
    # code = deepcopy(code)
    cfg: list[BasicBlock] = []
    starts = {0}
    funcs = set()
    calls = defaultdict(list)

    for instruction in code:
        t = type(instruction)
        if t in [GotoInstruction, CallInstruction, IfGotoInstruction]:
            if instruction.target:
                starts.add(instruction.target.id)
                if t == CallInstruction:
                    funcs.add((instruction.target.id - 1, code[instruction.target.id - 1].target.id))
                    calls[instruction.target.id - 1].append(instruction.id)
            starts.add(instruction.id + 1)
        elif t == AssignmentInstruction and type(instruction.rhs) == CallInstruction:
            if instruction.rhs.target:
                starts.add(instruction.rhs.target.id)
                funcs.add((instruction.rhs.target.id - 1, code[instruction.rhs.target.id - 1].target.id))
                calls[instruction.rhs.target.id - 1].append(instruction.id)
            starts.add(instruction.id + 1)
        elif t == ReturnInstruction:
            starts.add(instruction.id + 1)
    
    starts = sorted(list(starts))
    
    for i in range(len(starts)):
        block = BasicBlock()
        start = starts[i]
        end = starts[min(i + 1, len(starts) - 1)]
        block.instructions = code[start: end]
        for instruction in block.instructions:
            instruction.block = block
        cfg.append(block)
    end = BasicBlock()
    end.instructions = [code[-1]]
    code[-1].block = end
    cfg[-1] = end
    for i, block in enumerate(cfg):
        block.id = i

    
    for i, block in enumerate(cfg[:-1]):
        exit = block.instructions[-1]
        t = type(exit)
        if t == GotoInstruction:
            block.children().append(exit.target.block)
        elif t == IfGotoInstruction:
            block.children().append(exit.target.block)
            block.children().append(cfg[i + 1])
        elif t == CallInstruction:
            if exit.target:
                block.children().append(exit.target.block)
                #exit.target.block.children().append(cfg[block.id + 1])
        
                block.children().append(cfg[block.id + 1])
        elif t == AssignmentInstruction and type(exit.rhs) == CallInstruction:
            rhs = exit.rhs
            if  rhs.target:
                block.children().append(rhs.target.block)
                #rhs.target.block.children().append(cfg[block.id + 1])
            
                block.children().append(cfg[block.id + 1])
        elif t == ReturnInstruction:
            pass
            id = exit.id
            contain = list(filter(lambda f: f[0]<id<f[1], funcs))
            actual = min(contain, key=lambda f: f[1] - f[0])
            for id in calls[actual[0]]:
                block.children().append(code[id + 1].block)
        else:
            block.children().append(cfg[block.id + 1])

    return cfg

def dfs(node: Node):
    id = 0
    node.parent = None
    def dfs_rec(node: Node):
        nonlocal id
        node.id = id
        id += 1
        for child in node.children():
            if child is None:
                continue
            child.parent = node
            dfs_rec(child)
    dfs_rec(node)


def basicBlock2Graphviz(cfg: List[BasicBlock]) -> graphviz.Digraph:
    graph = graphviz.Digraph()
    queue = [cfg[0]]
    visited = dict.fromkeys(range(len(cfg)), False)
    while queue:
            block = queue.pop(0)
            graph.node(str(block.id), str(block))
            for child in block.children():
                if child.id < 0:
                    continue
                if not visited[child.id]:
                    queue.append(child)
                    visited[child.id] = True
                graph.edge(str(block.id), str(child.id))
    graph.node_attr['shape']='rectangle'
    return graph


def node2Graphviz(node: Node, merge=True) -> graphviz.Digraph:
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
                if child is None:
                    continue
                while (child.__class__ in merge_ops and len(child.ops) == 0) or (child.__class__ in merge_envelope and len(child.children()) == 1):
                    child = child.children()[0]
                queue.append(child)
                graph.edge(str(node.id), str(child.id))
    else:
        while queue:
            node = queue.pop(0)
            graph.node(str(node.id), str(node))
            for child in node.children():
                if child is None:
                    continue
                queue.append(child)
                graph.edge(str(node.id), str(child.id))
    return graph


