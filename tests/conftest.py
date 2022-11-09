import pytest
from sympy.physics.control.lti import TransferFunction
from sympy import simplify, pretty, Not, Eq


def pytest_assertrepr_compare(config: pytest.Config, op: str, left, right):
    if (
        op == "=="
        and isinstance(left, TransferFunction)
        and isinstance(right, TransferFunction)
    ):
        residual = simplify(left.to_expr() - right.to_expr())
        if residual != 0:
            return [
                "Comparing transfer functions:",
                *pretty(Not(Eq(left, right))).split('\n'),
                f"residual:",
                *pretty(residual).split('\n'),
            ]
