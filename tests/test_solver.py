from sympy import Integer, Float, Symbol, init_printing, simplify
from sympy.physics.control.lti import TransferFunction

from mna.element.passive import Resistor, Capacitor
from mna.element.active import VoltageSource
from mna.netlist.data import Netlist
from mna.netlist.solver import Solver

init_printing()

def test_rc_lpf():
    r = 100
    c = 1e-9
    net = Netlist(instances=[
        VoltageSource('V1', 1, 0, Symbol('v_in')),
        Resistor('R1', 1, 2, Integer(r)),
        Capacitor('C1', 2, 0, Float(c)),
    ])
    solver = Solver(net)
    print(solver.solve())
    h = solver.transfer_function(net.v[1], net.v[2])
    assert simplify(h.to_expr() - TransferFunction(1, r*c*Solver.s + 1, Solver.s).to_expr()) == 0