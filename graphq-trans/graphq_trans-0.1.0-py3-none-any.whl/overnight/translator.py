from antlr4 import *
from antlr4.InputStream import InputStream

from graphq_trans.overnight.OvernightLexer import OvernightLexer
from graphq_trans.overnight.OvernightParser import OvernightParser
from graphq_trans.overnight.OvernightListener import OvernightListener
from graphq_trans.overnight.IREmitter import IREmitter

from graphq_trans.utils import ErrorHandler


class Translator():
    def __init__(self):
        self.emitter = IREmitter()
        self.walker = ParseTreeWalker()
        self.error_listener = ErrorHandler() 

    def parser(self, input):
        input_stream = InputStream(input)
        lexer = OvernightLexer(input_stream)
        lexer.removeErrorListeners()
        lexer.addErrorListener(self.error_listener)    
           
        token_stream = CommonTokenStream(lexer)
        parser = OvernightParser(token_stream)
        parser.removeErrorListeners()
        parser.addErrorListener(self.error_listener)
        return parser.root()

    def to_ir(self, input):
        tree = self.parser(input)
        self.walker.walk(self.emitter, tree)
        ir = self.emitter.emit(tree)
        return ir

    
    