from collections import defaultdict
from collections.abc import Collection, Mapping
from typing import Generator, Iterator, Iterable, TypeVar, Generic

_I = TypeVar("_I")
_N = TypeVar("_N")
_E = TypeVar("_E")


class Adjacency(Generic[_I, _N, _E]):
    """Undirected adjacency list graph"""

    adjacency: Mapping[_I, Mapping[_I, list[_E]]]
    _nodes: dict[_I, _N]

    @property
    def n_nodes(self) -> int:
        return len(self._nodes)

    def __init__(self) -> None:
        self.adjacency = defaultdict(lambda: defaultdict(list))
        self._nodes = dict()

    def set_node(self, ix: _I, node: _N):
        self._nodes[ix] = node

    def get_node(self, ix: _I) -> _N | None:
        return self._nodes.get(ix, None)

    def add_edge(self, a: _I, b: _I, edge: _E):
        self.adjacency[a][b].append(edge)
        self.adjacency[b][a].append(edge)

    def get_edge(self, a: _I, b: _I) -> Collection[_E]:
        return self.adjacency[a][b]

    def nodes(self) -> Iterable[tuple[_I, _N]]:
        return self._nodes.items()

    def edges(self) -> Generator[tuple[_I, _I, _E], None, None]:
        for a, edges in self.adjacency.items():
            for b, weights in edges.items():
                for w in weights:
                    yield a, b, w

    def connected_to(self, node: _I) -> Iterable[tuple[_I, _E]]:
        for to, elems in self.adjacency[node].items():
            for el in elems:
                yield to, el

