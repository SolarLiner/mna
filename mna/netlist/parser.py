from parsec import *
import re
from typing import Callable, TypeVar
from sympy import Symbol, Float
from ..element import *
from .data import Netlist

__all__ = ["file", "line", "parse"]

_V = TypeVar('_V')

whitespace = regex(r'\s*', re.MULTILINE)
newline = string('\n')
lexeme: Callable[['Parser[_V]'], 'Parser[_V]'] = lambda p: p << whitespace

lparen = lexeme(string('('))
rparen = lexeme(string(')'))

ident = lexeme(regex(r'[rclvi][0-9]+', re.IGNORECASE))
nodeix = lexeme(regex(r'[0-9]+').parsecmap(int))

float = lexeme(
        regex(r'-?(0|[1-9][0-9]*)([.][0-9]+)?([eE][+-]?[0-9]+)?')
)
kw_symbolic = string('symbolic')

expr = regex(r'[^()]')

@generate("netlist")
def netlist():
    name = yield ident
    args = yield sepBy(nodeix, whitespace)
    value = yield kw_symbolic ^ float
    expr = value == 'symbolic' and Symbol(name, real=True, positive=True) or Float(value)

    match name[0].lower():
        case 'r': return Resistor(name, args[0], args[1], expr)
        case 'c': return Capacitor(name, args[0], args[1], expr)
        case 'l': return Inductance(name, args[0], args[1], expr)
        case 'v': return VoltageSource(name, args[0], args[1], expr)
        case 'i': return CurrentSource(name, args[0], args[1], expr)

@generate("opamp")
def opamp():
    name = yield lexeme(regex(r'o[0-9]+', re.IGNORECASE))
    n1 = yield nodeix
    n2 = yield nodeix
    n3 = yield nodeix

    return OpAmp(name, n1, n2, n3)

line = whitespace >> (opamp | netlist) << whitespace

file = sepBy1(line, newline).parsecmap(Netlist)

def parse(input: str) -> Netlist:
    return file.parse_strict(input.strip())