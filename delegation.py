from collections import OrderedDict as odict
import re


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
        invalid_char_match = re.search(r'[^\w ]', spec)
        if invalid_char_match:
            msg = (
                f'The spec of {repr(spec)} contains invalid character '
                f'"{invalid_char_match[0]}". Must only valid Python '
                'identifier characters and spaces.')
            raise ValueError(msg)

        attr_and_target = spec.split(' to ')

        if len(attr_and_target) < 2:
            msg = (
                f'The delegation spec of {repr(spec)} does not contain " to "')
            raise ValueError(msg)

        if len(attr_and_target) > 2:
            msg = (
                f'The delegation spec of {repr(spec)} contains " to " more '
                'than once')
            raise ValueError(msg)

        attr_and_target = tuple(map(str.strip, attr_and_target))

        for kwd in attr_and_target:
            if re.search(r'^\d', kwd):
                msg = (
                    f'Keyword {repr(kwd)} in spec starts with a digit, so it '
                    'is not valid as a Python keyword.')
                raise ValueError(msg)

        for kwd in attr_and_target:
            if ' ' in kwd:
                msg = (
                    f'Keyword {repr(kwd)} in spec contains a space, so it is '
                    'not valid as a Python keyword.')
                raise ValueError(msg)

        self.attr_name, self.target_name = attr_and_target

    def make_method(self):
        exec(f"""
@property
def {self.attr_name}(self):
    return self.{self.target_name}.{self.attr_name}
        """)
        return eval(f'{self.attr_name}')
