from dataclasses import dataclass, field
from typing import Iterator
from sympy import Symbol

from ..element.base import Element


@dataclass
class Netlist:
    instances: list[Element]
    nodes: int = field(init=False)
    vs_idx: list[int] = field(init=False)
    is_idx: list[int] = field(init=False)
    v: dict[int, Symbol] = field(init=False)
    i: dict[str, Symbol] = field(init=False)

    def __post_init__(self):
        self.n_nodes = max(n for i in self.instances for n in (i.n1, i.n2))
        self.vs_idx = [i for i, z in enumerate(self.instances) if z.is_voltage_source()]
        self.is_idx = [i for i, z in enumerate(self.instances) if z.is_current_source()]
        self.v = {i: Symbol(f"v_{i}") for i in range(1, self.n_nodes + 1)}
        self.i = {s.name: Symbol(f"i_{{{s.name}}}") for s in self.resolved_vs()}

    def resolved_vs(self) -> Iterator[Element]:
        return (self.instances[i] for i in self.vs_idx)

    def resolved_is(self) -> Iterator[Element]:
        return (self.instances[i] for i in self.is_idx)
