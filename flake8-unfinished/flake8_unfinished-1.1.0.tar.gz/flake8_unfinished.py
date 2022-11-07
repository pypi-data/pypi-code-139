import ast

from ezflake import ViolationType, Plugin, Visitor


__version__ = '1.1.0'


UNF001 = ViolationType('UNF001', "Don't raise '{}'")
UNF001_NAMES = ('NotImplementedError',)


class UnfinishedVisitor(Visitor):
    def visit_Raise(self, node: ast.Raise):
        name = None
        if isinstance(node.exc, ast.Name):
            name = node.exc.id
        elif isinstance(node.exc, ast.Call) and isinstance(node.exc.func, ast.Name):
            name = node.exc.func.id

        if name in UNF001_NAMES:
            self.violate_node(UNF001, node, name)
        self.generic_visit(node)


class UnfinishedPlugin(Plugin):
    name = __name__
    version = __version__
    visitors = [UnfinishedVisitor]
