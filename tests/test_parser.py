from mna.element import *
from mna.netlist.data import Netlist
from mna.netlist.parser import line, parse
from sympy import Float, Symbol
import parsec
import pytest


@pytest.mark.xfail(raises=parsec.ParseError)
@pytest.mark.parametrize(
    "input,expected",
    [
        ("V1 1 0 12", VoltageSource("V1", 1, 0, Float(12))),
        ("O1 0 2 3", OpAmp("O1", 0, 2, 3)),
        (
            "R1 1 2 symbolic",
            Resistor("R1", 1, 2, Symbol("R1", real=True, positive=True)),
        ),
    ],
)
def test_line(input: str, expected: Element):
    assert line.parse_strict(input) == expected


@pytest.mark.xfail(raises=parsec.ParseError)
@pytest.mark.parametrize(
    "input,expected",
    [
        (
            """
    V1 1 0 symbolic
    R1 1 2 symbolic
    C1 2 0 1e-9""",
            Netlist(
                instances=[
                    VoltageSource("V1", 1, 0, Symbol("V1")),
                    Resistor("R1", 1, 2, Symbol("R1")),
                    Capacitor("C1", 2, 0, Float("1e-9")),
                ]
            ),
        )
    ],
)
def test_netlist(input: str, expected: Netlist):
    assert parse(input) == expected
