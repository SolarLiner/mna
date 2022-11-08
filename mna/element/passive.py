from dataclasses import dataclass
from sympy import Expr, Integer
from .base import Element


class Passive(Element):
    """Passive element, one that does not emit extra voltage or current."""

    def vs_(self):
        return None

    def is_(self):
        return None

    def is_current_source(self) -> bool:
        return False

    def is_voltage_source(self) -> bool:
        return False

    def is_passive(self) -> bool:
        return True


@dataclass()
class Resistor(Passive):
    r: Expr

    def acceptance(self, s: Expr) -> Expr:
        return 1 / self.r


@dataclass()
class Capacitor(Passive):
    c: Expr

    def acceptance(self, s: Expr) -> Expr:
        return self.c * s


@dataclass()
class Inductance(Passive):
    l: Expr

    def acceptance(self, s: Expr) -> Expr:
        return 1 / (self.l * s)
