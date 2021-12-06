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
from os import remove
from typing import List
from parse.ast import DeclExprAST, NumExprAST, ExprAST
from tokenization.Tokens import TokenType, Token
from tokenization.Tokens import remove_tokens
from utils import ColorFormat as Coloring
from utils import colored_out as asxout
from utils import ClassUtils, LogOutput


class Parser(ClassUtils):
    '''Parser associated with AAST, parses tokens and matches
    them into Expressions (\sa ast.py@ExprAST) and handles reading tokens.'''
    def __init__(self, token_input: List[List[Token]], remove_spaces=True, log_levels=[]):
        '''Parameters:
        @token_input Tokens getting parsed into the AST.
        @log_levels  List of output priority levels, \sa utils.py@LogOutput.'''
        # NOTE Consider always removing the spaces, therefore also removing
        #      the parameter @param remove_spaces 
        self.token_input = token_input
        if remove_spaces:
            self.token_input = [remove_tokens(line, 0) for line in token_input]

        # Token Handling Attributes
        self.cur_tok = Token()
        self._line_index = 0
        self._token_index = 0

        # Logging System Setup ([vvv] Optionally Mutable Attribute) 
        self.log_importance_levels = log_levels
        self._log_out = LogOutput(self.log_importance_levels)

        # Map that stores the function calls for the associated token
        # \sa self.cur_tok
        self.AST_CALL_MAP = {
              TokenType.NUMBER: self.parse_num_expr,
              TokenType.LPAREN: self.parse_paren_expr,
              TokenType.EXCL  : self.parse_decl_expr,
        }

    def parse(self):
        '''Parses the given token_input'''
        self.cur_tok = self.get_next_token()

        if self.cur_tok.id != TokenType.EOF:
            self.parse_expr()

    def get_next_token(self) -> Token:
        """Static variable behaviour, upon call => moves to the next token.
        Note: Manages self._line_index & self._token_index."""
        # Line end    = reset token index, add 1 to line index
        # First token = return first token & don't subtract -1 from self._token_index
        if self._line_index >= len(self.token_input):
            self.cur_tok = Token(TokenType.EOF)
            return Token(TokenType.EOF)

        # Token Index Management => (Reset token index upon max. line len reached)
        #                        => (Add 1 to line index)
        if self._token_index == len(self.token_input[self._line_index]):
            self._line_index += 1
            self._token_index = 0
        self._token_index += 1

        # Check for special token indexes
        if self._line_index >= len(self.token_input):
            self.cur_tok = Token(TokenType.EOF)
            return Token(TokenType.EOF)
        elif self._line_index == 0 and self._token_index == 0:
            self._token_index += 1
            return self.token_input[0][0]

        self.cur_tok = self.token_input[self._line_index][self._token_index-1]
        self._log_out.src_log(2, 'Parser', f'{self._get_ctx()}, {self.cur_tok}')

        return self.cur_tok

    def _get_ctx(self) -> str:
        '''Returns the context, context as in:
        The current token index, in the given current line index.
        Format: @L[lineindex], @T[tokenindex]'''
        ctx_str = f'@L[{self._line_index+1}], @T[{self._token_index}]'
        return ctx_str

    def _get_last_ctx(self) -> str:
        '''Returns the token context before the current token (self.cur_tok),
        returns the current token context if the last token (-1) 
        would be a negative line index.'''
        line = self._line_index
        token = self._token_index - 1

        if token == 0 and line != 0:
            line -= 1
            token = len(self.token_input[line])
        
        return f'@L[{line+1}], @T[{token}]'

    # ::= AnyExpr
    def parse_expr(self) -> ExprAST | None:
        '''General parse expression function, parses all kinds of expressions,
        if there is no associated expr parse function => returns None.'''
        self._log_out.src_log(3, 'Parser', 'self.parse_expr() called.')
        parse_call = self.AST_CALL_MAP.get(self.cur_tok.id)
        if parse_call == None:
            asxout(
                Coloring.src_warning,
                'ParseExpr',
                f'{self.cur_tok} {self._get_ctx()} has no associated parse expr function.'
            )
            return parse_call # => None
        
        return parse_call() # => Expression

    # => 1  || [0-9] || int || TODO -> Implement float
    def parse_num_expr(self) -> NumExprAST:
        '''Parses every needed token for expression.'''
        expr = NumExprAST(self.cur_tok.value)
        self.get_next_token() # eat number literal
        
        return expr

    # ::= '(' expr, ... ')'
    def parse_paren_expr(self) -> List[ExprAST] | List:
        '''Parses expr(s) in between of parenthesis.'''
        self._log_out.src_log(3, 'Parser', 'self.parse_paren_expr() called.')
        expressions = []
        
        self.get_next_token() # eat '('
        if self.cur_tok.id != TokenType.RPAREN:
            # Parse every in-paren expression, until RPAREN ends it
            while True:
                cur_expr = self.parse_expr()
                if cur_expr != None:
                    expressions.append(cur_expr)
                
                if self.cur_tok.id == TokenType.RPAREN:
                    break
                elif self.cur_tok.id != TokenType.COMMA:
                    if self.cur_tok.id != TokenType.SPACE:
                        asxout(
                            Coloring.src_error,
                            'ParseParenExpr', 
                            f'Expected [\')\'] or [\',\']; {self._get_last_ctx()}'
                        )

                self.get_next_token()
        else:
            return expressions # empty in this case
        self.get_next_token()

        return expressions # not empty in this case

    def parse_decl_expr(self) -> DeclExprAST:
        '''Parses the function declaration expression.
        Called when token is TokenType.DEF'''
        self._log_out.src_log(3, 'Parser', 'self.parse_declr_expr() called.')
        # Expression = def function_name(args):
        func_name = None
        func_args = None

        self.get_next_token() # eat '!'
        func_name = self.cur_tok.value

        self.get_next_token() # should be '(', if not => Error
        if self.cur_tok.id != TokenType.LPAREN:
            asxout(
                Coloring.src_error,
                'ParseDeclExpr', f'Expected [\'(\']; {self._get_ctx()}'
            )
        
        # Calls @method self.parse_paren_expr()
        func_args = self.parse_expr()

        if self.cur_tok.id != TokenType.COLON:
            asxout(
                Coloring.src_error,
                'ParseDeclrExpr', f'Expected [\':\']; {self._get_ctx()}'
            )

        return DeclExprAST(name=func_name, args=func_args)
