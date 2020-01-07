import json
from enum import Enum
from functools import partial

from multipledispatch import dispatch


def signed_num_bin_len(num):
    return len("{:+b}".format(num))


def unsigned_num_bin_len(num):
    return len("{:b}".format(num))


def get_hcl_expr_by_name(packed_module, name):
    table = packed_module.named_expr_chain.named_expr_chain_head \
        .named_expr_holder.named_expression_table
    expr_id = get_key_by_value(table, name)
    return get_hcl_expr_by_id(expr_id)


def get_hcl_expr_by_id(expr_id):
    from py_hcl.core.expr import ExprTable
    return ExprTable.table[expr_id]


def get_key_by_value(dct, value):
    return list(dct.keys())[list(dct.values()).index(value)]


def json_serialize(cls=None, json_fields=()):
    def rec(v):
        if hasattr(v, "json_obj"):
            return v.json_obj()
        elif isinstance(v, dict):
            return {k: rec(v) for k, v in v.items()}
        elif isinstance(v, (list, tuple)):
            return [rec(v) for v in v]
        elif isinstance(v, Enum):
            return v.name
        return v

    def serialize(self):
        return json.dumps(self.json_obj(), indent=2)

    def _(_cls, _json_fields):
        def js(self):
            if len(_json_fields) == 0:
                kv = vars(self)
            else:
                kv = {f: vars(self)[f] for f in _json_fields}

            return {k: rec(v) for k, v in kv.items()}

        _cls.json_obj = js
        _cls.__str__ = serialize
        return _cls

    if cls:
        return _(cls, json_fields)

    return partial(_, _json_fields=json_fields)


@dispatch()
def _fm(vd: dict):
    ls = ['{}: {}'.format(k, _fm(v)) for k, v in vd.items()]
    fs = _iter_repr(ls)
    return '{%s}' % (''.join(fs))


@dispatch()
def _fm(v: list):
    ls = [_fm(a) for a in v]
    fs = _iter_repr(ls)
    return '[%s]' % (''.join(fs))


@dispatch()
def _fm(v: tuple):
    ls = [_fm(a) for a in v]
    fs = _iter_repr(ls)
    return '(%s)' % (''.join(fs))


@dispatch()
def _fm(v: object):
    return str(v)


def _iter_repr(ls):
    if len(ls) <= 1:
        fs = ''.join(ls)
    else:
        fs = ''.join(['\n  {},'.format(_indent(l)) for l in ls]) + '\n'
    return fs


def _indent(s: str) -> str:
    s = s.split('\n')
    return '\n  '.join(s)
