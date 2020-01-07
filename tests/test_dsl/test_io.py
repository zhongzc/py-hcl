import pytest

from py_hcl.core.expr.error import ExprError
from py_hcl.core.type import HclType
from py_hcl.core.type.bundle import BundleT
from py_hcl.dsl.expr.io import IO, Input, Output, io_extend
from py_hcl.dsl.module import Module
from py_hcl.dsl.tpe.uint import U
from py_hcl.utils import get_hcl_expr_by_name


class A(Module):
    io = IO(
        i=Input(U.w(8)),
        o=Output(U.w(8)))

    io.o <<= io.i


def test_io():
    io = get_hcl_expr_by_name(A.packed_module, 'io')
    assert isinstance(io.hcl_type, BundleT)
    assert len(io.hcl_type.fields) == 2


def test_io_inherit_basis():
    class B(A):
        io = io_extend(A)(
            i1=Input(U.w(9)),
        )
        io.o <<= io.i1

    io = get_hcl_expr_by_name(B.packed_module, 'io')
    assert isinstance(io.hcl_type, BundleT)
    assert len(io.hcl_type.fields) == 3


def test_io_inherit_override():
    class B(A):
        io = io_extend(A)(
            i=Input(U.w(9)),
        )
        io.o <<= io.i

    io = get_hcl_expr_by_name(B.packed_module, 'io')
    assert isinstance(io.hcl_type, BundleT)
    assert len(io.hcl_type.fields) == 2


def test_io_no_wrap_io():
    with pytest.raises(ExprError, match='^.*Input.*Output.*$'):
        class A(Module):
            io = IO(i=HclType())

    with pytest.raises(ExprError, match='^.*Input.*Output.*$'):
        class A(Module):
            io = IO(
                i=HclType(),
                o=Output(HclType()))

    with pytest.raises(ExprError, match='^.*Input.*Output.*$'):
        class A(Module):
            io = IO(
                i=Input(HclType()),
                o=HclType())
