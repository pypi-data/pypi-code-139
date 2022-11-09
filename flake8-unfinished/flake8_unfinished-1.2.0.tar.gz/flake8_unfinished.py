from __future__ import annotations

import ast

from ezflake import ViolationType, Plugin, Visitor
from ezflake.utils import all_return


__version__ = '1.2.0'


UNF001 = ViolationType('UNF001', '`raise {}` found')
UNF001.names = ('NotImplementedError',)

UNF002 = ViolationType('UNF002', 'Reference to `{}` found')
UNF002.names = UNF001.names  # (,)

UNF100 = ViolationType('UNF100', 'Only useless statements in the function body: {}')


class UnfinishedVisitor(Visitor):
    def visit_Raise(self, node: ast.Raise):
        name = None
        if isinstance(node.exc, ast.Name):
            name = node.exc.id
        elif isinstance(node.exc, ast.Call) and isinstance(node.exc.func, ast.Name):
            name = node.exc.func.id

        if name in UNF001.names:
            self.violate_node(UNF001, node, name)
        self.generic_visit(node)

    def visit_Name(self, node: ast.Name):
        name = node.id
        if name in UNF002.names:
            self.violate_node(UNF002, node, name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        assert node.body
        items = all_return(is_useless(stmt) for stmt in node.body)
        if items:
            self.violate_node(UNF100, node, ', '.join(items))
        self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef


class UnfinishedPlugin(Plugin):
    name = __name__
    version = __version__
    visitors = [UnfinishedVisitor]


def is_useless(stmt: ast.stmt) -> str | bool:
    if isinstance(stmt, ast.Pass):
        return '`pass`'
    elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Constant):
        if isinstance(stmt.value.value, str):
            return 'docstring'
        elif stmt.value.value is Ellipsis:
            return '`...`'
    return False
