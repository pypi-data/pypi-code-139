from antlr4 import *
from antlr4.InputStream import InputStream

from graphq_trans.sparql.SparqlLexer import SparqlLexer
from graphq_trans.sparql.SparqlParser import SparqlParser
from graphq_trans.sparql.SparqlListener import SparqlListener
from graphq_trans.sparql.IREmitter import IREmitter

from graphq_trans.utils import ErrorHandler


class Translator():
    def __init__(self):
        self.emitter = IREmitter()
        self.walker = ParseTreeWalker()
        self.error_listener = ErrorHandler()

    def parse(self, input):
        input_stream = InputStream(input)
        lexer = SparqlLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(self.error_listener)    
           
        token_stream = CommonTokenStream(lexer)
        parser = SparqlParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(self.error_listener)
        return parser.query()

    def to_ir(self, input):
        tree = self.parse(input)
        self.walker.walk(self.emitter, tree)
        ir = self.emitter.emit(tree)
        return ir
