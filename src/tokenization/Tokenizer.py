# ===================================
# - Official Astro Source Code -
# (\sa: https://github.com/xyLotus/Astro/blob/master/src/compiler/tokenizer.py)
# ===================================
# -*- coding: utf-8 -*-
# ===================================
"""Contains the lexer that returns the tokens 
for each line in the passed file @class Lexer."""
# ===================================
# Dunder Credentials
# ===================================
__author__  = 'xyLotus'
__version__ = '0.1.0' 
# ===================================
# Imports
# ===================================
from tokenization.Tokens import Token, TokenType
from tokenization.AstroFile import AstroFile 


class Tokenizer:
    """ This class tokenizes the given files
    given in @member h_file and returns the tokens
    per line uncompressed and raw. """

    def __init__(self, h_file: AstroFile, save_tokens=True):
        """Members & Usage:
        @member file = file to be tokenized,
        @member tokens = token list (used in @method tokenize)"""
        self.is_compressed = False
        self.h_file = h_file
        self.tokens = []
        self.content = self.h_file.content

    def output_tokens(self):
        """ Outputs tokens in human easy-to-read format
        for debugging and readability purposes. """
        for line in self.tokens:
            for tok in line:
                print(tok, end=' ')
            print()

    def get_context(self):
        """ Returns context in dict format providing
        line, source and tokens. Should probably only
        be called when tokens are compressed. """
        if not self.is_compressed:
            print(f'[Tokenizer-Error]: Compress tokens with compress();')
            exit(1)

        context_list = []
        sources = self.content.split('\n')
        for i, line in enumerate(self.tokens):
            context_list.append({
                'line': i + 1,
                'source': sources[i],   
                'tokens': self.tokens[i]
            })

        return context_list

    def tokenize(self) -> list:
        """ Tokenizes given file by accessing file handle
        @member h_file (AstroFile) and storing the tokens in @member tokens."""
        toks = []

        type_map = {
            ' ':  TokenType.SPACE,
            '!':  TokenType.EXCL,
            '(':  TokenType.LPAREN,
            ')':  TokenType.RPAREN,
            '<':  TokenType.LCHEV,
            '>':  TokenType.RCHEV,
            ':':  TokenType.COLON,
            ',':  TokenType.COMMA,
            '\'': TokenType.QUOTE,
            '"':  TokenType.DBQUOTE,
            '=':  TokenType.ASSIGN,
        }

        for line in self.content.split('\n'):
            line_buffer = []
            for ch in line:
                typ = type_map.get(ch, TokenType.SYM)
                line_buffer.append(Token(typ, ch))
            toks.append(line_buffer)

        # Compress all required tokens
        toks = self._compress(toks, TokenType.SYM, TokenType.NAME)

        self.tokens = toks
        
        # Save tokens to log file if @param save_tokens is True
        with open('_asx_token_log.log', 'w') as f:   
            f.write("========================================================================\n")
            f.write(f"Auto-generated Astro tokenization log of file: [{self.h_file.file_name}]\n")
            f.write("========================================================================\n")
            for line in toks:
                for token in line:
                    f.write(str(token) + ' ')
                f.write('\n')

        return toks

    def _compress(self, tokens: list, from_: int, to_: int) -> list:
        """ Compresses the tokens into sub-tokens which
        are smaller, ready for compilation and syntax lexing,
        overwriting @member self.compressed_tokens. """
        self.is_compressed = True

        # compress token sets line by line
        toks = []
        for line in tokens:
            value_buf = ""
            line_buf = []

            # line compression process
            for i, tok in enumerate(line):
                if tok.id != from_:
                    line_buf.append(tok)

                if i != len(line) - 1:  # End of Token Set!
                    if tok.id == from_ and line[i+1].id == from_:
                        value_buf += tok.value
                    elif tok.id == from_ and line[i+1].id != from_:
                        value_buf += tok.value

                        line_buf.append(Token(id_=to_, value=value_buf))
                        value_buf = ""
                elif tok.id == from_:
                    value_buf += tok.value
                    
                    line_buf.append(Token(id_=to_, value=value_buf))
                    value_buf = ""  # clear buffer

            toks.append(line_buf)

        return toks