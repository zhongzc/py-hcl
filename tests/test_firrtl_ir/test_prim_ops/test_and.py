from py_hcl.firrtl_ir.expr.prim_ops import And
from py_hcl.firrtl_ir.shortcuts import uw, u, w, s
from py_hcl.firrtl_ir.type import UIntType, SIntType
from tests.test_firrtl_ir.utils import serialize_equal
from .helper import OpCase, basis_tester, \
    encounter_error_tester, type_wrong_cases_2_args_gen, max_width


def args(*arg_types):
    class C:
        @staticmethod
        def tpe(res_type):
            return OpCase(And).arg_types(*arg_types).res_type(res_type)

    return C


and_basis_cases = [
    args(UIntType, UIntType).tpe(lambda x, y: uw(max_width(x, y))),
    args(SIntType, SIntType).tpe(lambda x, y: uw(max_width(x, y))),
]

and_type_wrong_cases = type_wrong_cases_2_args_gen(And)

and_width_wrong_cases = [
    args(UIntType, UIntType).tpe(lambda x, y: uw(max_width(x, y) + 1)),
    args(SIntType, SIntType).tpe(lambda x, y: uw(max_width(x, y) + 1)),
    args(UIntType, UIntType).tpe(lambda x, y: uw(max_width(x, y) - 1)),
    args(SIntType, SIntType).tpe(lambda x, y: uw(max_width(x, y) - 1)),
]


def test_and():
    basis_tester(and_basis_cases)
    encounter_error_tester(and_type_wrong_cases)
    encounter_error_tester(and_width_wrong_cases)
    serialize_equal(And([u(20, w(5)), u(15, w(4))], uw(5)),
                    'and(UInt<5>("h14"), UInt<4>("hf"))')
    serialize_equal(And([s(-20, w(6)), s(-15, w(5))], uw(6)),
                    'and(SInt<6>("h-14"), SInt<5>("h-f"))')
