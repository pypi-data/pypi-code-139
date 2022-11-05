from antlr4 import *
from antlr4.InputStream import InputStream

from graphq_trans.cypher.CypherLexer import CypherLexer
from graphq_trans.cypher.CypherParser import CypherParser
from graphq_trans.cypher.CypherParserListener import CypherParserListener
from graphq_trans.cypher.IREmitter import IREmitter

from graphq_trans.utils import ErrorHandler


class Translator():
    def __init__(self):
        self.emitter = IREmitter()
        self.walker = ParseTreeWalker()
        self.error_listener = ErrorHandler()

    def parse(self, input):
        input_stream = InputStream(input)
        lexer = CypherLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(self.error_listener)    
           
        token_stream = CommonTokenStream(lexer)
        parser = CypherParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(self.error_listener)
        return parser.root()

    def to_ir(self, input):
        tree = self.parse(input)
        self.walker.walk(self.emitter, tree)
        ir = self.emitter.emit(tree)
        return ir