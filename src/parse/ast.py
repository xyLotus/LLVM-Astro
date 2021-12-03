# ===================================
# - Official Astro Source Code -
# ===================================
'''Contains the Astro Abstract Syntax Tree (AAST/AST) hierarchy.'''
# ===================================
# Dunder Credentials
# ===================================
__author__  = 'xyLotus'
__version__ = '.' 
# ===================================
# Imports
# ===================================
from abc import ABC


#! Base Class
class ExprAST(ABC):
    '''The abstract base class inheriting into all
    expressionistic AST subclasses.'''
    def __str__(self):
        class_name = str(ExprAST.__dict__['__dict__']).split(' ')[3].replace('\'', '')
        return f'{class_name}()'

class VarExprAST(ExprAST):
    '''A expression subclass for referencing variable names.'''
    def __init__(self, value: str):  
        self.value = value 


class NumExprAST(ExprAST):
    '''A expression subclass for number literals.'''
    def __init__(self, value: int):
        self.value = value


class BinExprAST(ExprAST):
    '''A expression subclass for binary operators'''
    def __init__(self, operator: str):
        self.operator = operator


class CallExprAST(ExprAST):
    '''A expression subclass for function calls.'''
    def __init__(self, caller: str, args: list):
        '''Members:
        @member caller - Name of function being called
        @member args   - Arguments being passed to called function.'''
        self.caller = caller
        self.args = args


class DeclExprAST(ExprAST):
    '''A expression subclass for function declarations.'''
    def __init__(self, name: str, args: list):
        '''Members:
        @member name - Name of function
        @member args - Arguments declared in function'''
        self.name = name
        self.args = args


class FuncExprAST(ExprAST):
    '''A expression subclass for function definitions.'''
    def __init__(self, declaration: DeclExprAST, content: str):
        # Declaration may not be seperate
        self.declaration = declaration 
        self.content = content

