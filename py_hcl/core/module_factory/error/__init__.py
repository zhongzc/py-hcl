from py_hcl.core.error import CoreError


def set_up():
    ModuleError.append({
        'NotContainsIO': {
            'code': 100,
            'value': ModuleError('io attribute is required in Module')},
    })


class ModuleError(CoreError):
    @staticmethod
    def not_contains_io(msg):
        return ModuleError.err('NotContainsIO', msg)


set_up()
