# ===================================
# - Official Astro Source Code -
# ===================================
"""Main entrypoint of LLVM-Astro. """
# ===================================
# Dunder Credentials
# ===================================
__author__  = 'xyLotus'
# ===================================
# Imports
# ===================================
from tokenization.Tokenizer import TokenType, Tokenizer, Token
from tokenization.AstroFile import AstroFile
from parse.parser import Parser
from parse.ast import *
from utils import colored_out as asxout
from utils import ColorFormat as Coloring
import sys


# Entrypoint
def main(): 
    # Argument Error Handling (TODO -> Implement argparse).
    assert len(sys.argv) != 0, '[Argpass-Error-FATAL]: No src Arguments given.'
    assert len(sys.argv) != 1, '[Argpass-Error-FATAL]: No input file given.'

    # File Handle establishment & Tokenization
    file_handle = AstroFile(sys.argv[1], cleanup=True)
    tokenizer = Tokenizer(file_handle, save_tokens=True)
    tokens = tokenizer.tokenize()
    asxout(Coloring.src_log, 'Tokenizer', 'Tokenization finished.\n')

    # Parsing with the AST
    parser = Parser(tokens)
    token_buffer = Token()
    while token_buffer.id != TokenType.EOF:
        token_buffer = parser.get_next_token()
    
    print()
    asxout(Coloring.src_log, 'Parser', 'End of file reached.')

    print(parser.cur_tok)
    print(NumExprAST.__dict__)
    expr = parser.parse_expr()
    print(expr)


if __name__ == '__main__':
    main()