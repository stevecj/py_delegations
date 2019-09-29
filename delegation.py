from collections import OrderedDict as odict


class DelegatesAttrsType(type):

    @classmethod
    def __prepare__(mcl, name, bases):
        super().__prepare__(name, bases)
        delegations = []

        def delegate(spec):
            delegation = Delegation(spec)
            delegations.append(delegation)

        namespace = odict()
        namespace['_delegations'] = delegations
        namespace['delegate'] = delegate

        return namespace

    def __init__(cls, name, base, namespace):
        for delegation in namespace.get('_delegations', []):
            method = delegation.make_method()
            setattr(cls, delegation.attr_name, method)


class DelegatesAttrs(metaclass=DelegatesAttrsType):
    pass


class Delegation:
    def __init__(self, spec):
        attr_and_target = spec.split(' to ')
        self.attr_name, self.target_name = attr_and_target

    def make_method(self):
        exec(f"""
@property
def {self.attr_name}(self):
    return self.{self.target_name}.{self.attr_name}
        """)
        return eval(f'{self.attr_name}')
