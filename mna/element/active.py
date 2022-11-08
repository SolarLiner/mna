from dataclasses import dataclass
from sympy import Expr, Integer

from .base import Element


@dataclass()
class VoltageSource(Element):
    vs: Expr

    def vs_(self) -> Expr:
        return self.vs

    def b_coefficient(self, node: int) -> int:
        if node == self.n1:
            return 1
        if node == self.n2:
            return -1
        return 0


@dataclass()
class CurrentSource(Element):
    i_s: Expr

    def is_(self) -> Expr:
        return self.i_s


@dataclass()
class OpAmp(Element):
    n3: int

    def vs_(self) -> Expr | None:
        return Integer(0)

    def connected_to(self, node: int) -> int:
        return node in {self.n1, self.n2, self.n3}

    def b_coefficient(self, node: int) -> int:
        if node == self.n2:
            return 1
        if node == self.n1 or node == self.n3:
            return -1
        return 0
