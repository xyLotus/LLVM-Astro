#!/usr/bin/python3.10

# ===================================
# - Official Astro Source Code -
# ===================================
'''Contains AAST associated parser.'''
# ===================================
# Dunder Credentials
# ===================================
__author__  = 'xyLotus'
__version__ = '.' 
# ===================================
# Imports
# ===================================
from typing import List
from parse.ast import NumExprAST, ExprAST
from tokenization.Tokens import TokenType, Token
from utils import ColorFormat as Coloring
from utils import colored_out as asxout

class Parser:
    """Parser associated with AAST, parses tokens and handles reading tokens. """
    def __init__(self, token_input: List[List[Token]]):
        self.token_input = token_input
        self._line_index = 0
        self._token_index = 0
        self.cur_tok = Token()

        self.AST_CALL_MAP = {
              TokenType.NUMBER: self.parse_num_expr,
              TokenType.LPAREN: self.parse_paren_expr
        }

    def get_next_token(self) -> Token:
        """Static-alike behaviour, upon call => moves to the next token."""
        # Line end    = reset token index, add 1 to line index
        # First token = return first token & don't subtract -1 from self._token_index
        if self._line_index >= len(self.token_input):
            return Token(TokenType.EOF)

        # Token Index Management => (Reset token index upon max. line len reached)
        #                        => (Add 1 to line index)
        if self._token_index == len(self.token_input[self._line_index]):
            self._line_index += 1
            self._token_index = 0
        self._token_index += 1

        # Check for special token indexes
        if self._line_index >= len(self.token_input):
            return Token(TokenType.EOF)
        elif self._line_index == 0 and self._token_index == 0:
            self._token_index += 1
            return self.token_input[0][0]

        self.cur_tok = self.token_input[self._line_index][self._token_index-1]
        asxout(Coloring.src_log, 'Parser', f'Tok Line IDX={self._line_index}')
        asxout(Coloring.src_log, 'Parser', f'Tok IDX={self._token_index}')
        asxout(Coloring.src_log, 'Parser', f'Current Token = {self.cur_tok}')

        return self.cur_tok

    def parse_expr(self) -> ExprAST:
        '''General parse expression function, parses all kinds of expressions,
        throws exception if the TokenType does not have a associated expr parse function.'''
        # Assign parse_func to potential parse function corresponding to the current token
        assert (parse_func := self.AST_CALL_MAP.get(self.cur_tok.id)) != None \
            , Coloring.src_error('Parser', f'No expression associated with token [{self.cur_tok}]')
        
        return parse_func()

    # => 1  || [0-9] || int || TODO -> Implement float
    def parse_num_expr(self) -> NumExprAST:
        '''Parses every needed token for expression.'''
        expr = NumExprAST(self.cur_tok.value)
        return expr

    # => ( expr )
    def parse_paren_expr(self):
        '''Parses expr in between of parenthesis.'''
        self.get_next_token() # eat '('
        expr = self.parse_expr
