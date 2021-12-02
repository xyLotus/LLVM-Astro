# ===================================
# - Official Astro Source Code -
# ===================================
# -*- coding: utf-8 -*-
# ===================================
"""Main entrypoint of LLVM-Astro"""
# ===================================
# Dunder Credentials
# ===================================
__author__  = 'xyLotus'
# ===================================
# Imports
# ===================================
from tokenization.Tokenizer import Tokenizer
from tokenization.AstroFile import AstroFile 
import sys

# Entrypoint
def main():
    # Argument Error Handling (TODO -> Implement argparse).
    assert len(sys.argv) != 0, "[Argpass-Error-FATAL]: No src Arguments given."
    assert len(sys.argv) != 1, "[Argpass-Error-FATAL]: No input file given."

    # File Handle establishment & Tokenization
    file_handle = AstroFile(sys.argv[1], cleanup=True)
    tokenizer = Tokenizer(file_handle, save_tokens=True)
    tokens = tokenizer.tokenize()


if __name__ == '__main__':
    main()