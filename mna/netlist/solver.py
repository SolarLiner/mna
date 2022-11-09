from collections import ChainMap
from dataclasses import dataclass, field
from functools import cached_property
from typing import ClassVar, Mapping, TypeVar
from sympy import BlockMatrix, Eq, Expr, Symbol, Matrix, diag, zeros, solve
from sympy.physics.control.lti import TransferFunction
from ..element.base import Element
from ..element.active import OpAmp
from ..adj import Adjacency
from .data import Netlist


@dataclass()
class Solver:
    s: ClassVar = Symbol("s", complex=True)
    netlist: Netlist
    circ: Adjacency[int, Symbol, Element] = field(init=False)

    def __post_init__(self) -> None:
        self.circ = Adjacency()

        for i, s in self.netlist.v.items():
            self.circ.set_node(i, s)

        for z in self.netlist.instances:
            self.circ.add_edge(z.n1, z.n2, z)
            if isinstance(z, OpAmp):
                self.circ.add_edge(z.n1, z.n3, z)
                self.circ.add_edge(z.n2, z.n3, z)

    @cached_property
    def G(self) -> Matrix:
        d = diag(
            [
                sum(z.acceptance(self.s) for _,z in self.circ.connected_to(node) if z.is_passive())
                for node,_ in self.circ.nodes()
            ],
            unpack=True,
        )
        m = Matrix(
            [
                [
                    sum(-z.acceptance(self.s) for z in self.circ.get_edge(a, b) if z.is_passive())
                    for b,_ in self.circ.nodes()
                ]
                for a,_ in self.circ.nodes()
            ]
        )
        return d + m

    @cached_property
    def B(self) -> Matrix:
        return Matrix(
            [
                [s.b_coefficient(k) for s in self.netlist.resolved_vs()]
                for k,_ in self.circ.nodes()
            ]
        )

    @cached_property
    def C(self) -> Matrix:
        return Matrix(
            [
                [s.b_coefficient(k) for k,_ in self.circ.nodes()]
                for s in self.netlist.resolved_vs()
            ]
        )

    @cached_property
    def D(self) -> Matrix:
        return zeros(len(self.netlist.vs_idx))

    def get_matrix(self) -> Matrix:
        return BlockMatrix([[self.G, self.B], [self.C, self.D]]).as_explicit()

    @cached_property
    def x(self) -> Matrix:
        v = list(self.netlist.v.values())
        j = list(self.netlist.i.values())
        return Matrix(v + j)

    @cached_property
    def z(self) -> Matrix:
        i = [
            sum(
                z.is_()
                for _,z in self.circ.connected_to(node)
                if z.is_current_source()
            )
            for node in self.circ.nodes()
        ]
        e = [z.vs_() for z in self.netlist.resolved_vs()]
        return Matrix(i + e)

    def get_equation(self) -> Eq:
        return Eq(self.x, self.get_matrix().inv() * self.z)

    def solve(self) -> ChainMap[Symbol, Expr]:
        return ChainMap(
            *solve(
                self.get_equation(),
                *self.netlist.v.values(),
                *self.netlist.i.values(),
                dict=True
            )
        )

    def transfer_function(self, vin: Symbol, vout: Symbol) -> TransferFunction:
        solutions = self.solve()
        # output = solutions[vout].subs(exclude(solutions, vout))
        output = (solutions[vout] / vin).subs(solutions).simplify()
        return TransferFunction.from_rational_expression(output, self.s)

_K = TypeVar('_K')
_T = TypeVar('_T')

def exclude(d: Mapping[_K, _T], k: _K) -> dict[_K, _T]:
    return {ik: iv for ik, iv in d.items() if ik != k}