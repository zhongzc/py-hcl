from .utils import type_in
from ..expr.literal import SIntLiteral, SIntType, UIntLiteral, UIntType
from ..utils import signed_num_bin_len


class LiteralTypeChecker(object):
    literal_checker_map = {}

    @staticmethod
    def check(op_obj):
        try:
            return LiteralTypeChecker.literal_checker_map[type(op_obj)](op_obj)
        except KeyError:
            raise NotImplementedError(type(op_obj))


def checker(literal):
    def f(func):
        LiteralTypeChecker.literal_checker_map[literal] = func
        return func

    return f


@checker(UIntLiteral)
def _(uint):
    if not type_in(uint.tpe, UIntType):
        return False

    at_least_width = signed_num_bin_len(uint.value) - 1
    at_least_width += (1 if uint.value < 0 else 0)
    if at_least_width > uint.tpe.width.width:
        return False

    return True


@checker(SIntLiteral)
def _(sint):
    if not type_in(sint.tpe, SIntType):
        return False

    if signed_num_bin_len(sint.value) > sint.tpe.width.width:
        return False

    return True