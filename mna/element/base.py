from abc import abstractmethod
from dataclasses import dataclass

from sympy import Expr, Integer


@dataclass()
class Element:
    """Circuit element. Representation of a Netlist input line."""

    name: str
    n1: int
    n2: int

    def acceptance(self, s: Expr) -> Expr:
        """Element acceptance, or inverse impedance. To be overriden by all supported elements."""
        raise NotImplementedError()
        # return Integer(0)

    def vs_(self) -> Expr | None:
        """Optional voltage source emitted by the element."""
        return None

    def is_(self) -> Expr | None:
        """Optional current source emitted by the element."""
        return None

    def is_voltage_source(self) -> bool:
        """Derived method to check if the element is a voltage source."""
        return self.vs_() is not None

    def is_current_source(self) -> bool:
        """Derived method to check if the element is a current source."""
        return self.is_() is not None

    def is_passive(self) -> bool:
        """Derived method to check that the element is neither a current nor a current source."""
        return not self.is_voltage_source() and not self.is_current_source()

    def connected_to(self, node: int) -> int:
        """Is the element connected to the given node?"""
        return node == self.n1 or node == self.n2

    def b_coefficient(self, node: int) -> int:
        """B coefficient for this node: 1 if the node is connected to the positive side of this dipole, -1 if the node is connected to the negative side of this dipole. 0 otherwise."""
        return 0
