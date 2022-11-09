from sympy import Integer, Float, Symbol, symbols, init_printing, simplify
from sympy.physics.control.lti import TransferFunction

from mna.element.passive import Resistor, Capacitor
from mna.element.active import OpAmp, VoltageSource
from mna.netlist.data import Netlist
from mna.netlist.solver import Solver

import pytest

init_printing(use_unicode=True)

vin, r, c = symbols("V_in R C", real=True, positive=True)
z1, z2, z3, z4 = symbols("Z_1 Z_2 Z_3 Z_4", complex=True)

net_rc = Netlist(
    [
        VoltageSource("V1", 1, 0, Symbol("v_in")),
        Resistor("R1", 1, 2, r),
        Capacitor("C1", 2, 0, c),
    ]
)
expected_rc = TransferFunction(1, r * c * Solver.s + 1, Solver.s)

net_sk = Netlist(
    [
        VoltageSource("Vin", 1, 0, vin),
        Resistor("Z_1", 1, 2, z1),
        Resistor("Z_2", 2, 3, z2),
        Resistor("Z_3", 4, 2, z3),
        Resistor("Z_4", 0, 3, z4),
        OpAmp("O_1", 3, 4, 4),
    ]
)
expected_sk = TransferFunction(z3 * z4, z1 * z2 + z3 * (z1 + z2) + z3 * z4, Solver.s)

# ====== TESTS ========


@pytest.mark.parametrize(
    ["netlist", "expected", "vin", "vout"],
    [
        (net_rc, expected_rc, net_rc.v[1], net_rc.v[2]),
        (net_sk, expected_sk, net_sk.v[1], net_sk.v[4]),
    ],
)
def test_solver(
    netlist: Netlist, expected: TransferFunction, vin: Symbol, vout: Symbol
):
    solver = Solver(netlist)
    h = solver.transfer_function(vin, vout)
    assert expected == h
