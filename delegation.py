from collections import OrderedDict as odict
import re


class DelegatesAttrsType(type):

    @classmethod
    def __prepare__(mcl, name, bases):
        super().__prepare__(name, bases)

        namespace = odict()

        def delegate(*args, **kwargs):
            _delegate(namespace, *args, **kwargs)

        namespace['delegate'] = delegate

        return namespace


class DelegatesAttrs(metaclass=DelegatesAttrsType):
    pass


def _delegate(namespace, spec, setter=False):
    delegation = Delegation(spec, setter)
    method_def = f"""
@property
def {delegation.name}(self):
    return self.{delegation.target_name}.{delegation.attr_name}
"""
    if delegation.with_setter:
        method_def += f"""
@{delegation.name}.setter
def {delegation.name}(self, new_value):
    self.{delegation.target_name}.{delegation.attr_name} = new_value
"""
    exec(method_def, {}, namespace)


class Delegation:
    SPEC_DOES_NOT_FOLLOW_PATTERN_FMT = (
        'The spec value of {} does not follow the pattern of "<keyword> to'
        ' <keyword>" or "<keyword> to <keyword> as <keyword>".')

    def __init__(self, spec, with_setter=False):
        spec = spec.strip()

        invalid_char_match = re.search(r'[^\w ]', spec)
        if invalid_char_match:
            msg = (
                f'The spec of {repr(spec)} contains invalid character '
                f'"{invalid_char_match[0]}". Must only contain valid Python '
                'identifier characters and spaces.')
            raise ValueError(msg)

        attr_name_and_rest_match = re.search(r'^(\w+) +to +(\w.*)', spec)
        if not attr_name_and_rest_match:
            raise ValueError(
                self.SPEC_DOES_NOT_FOLLOW_PATTERN_FMT.format(repr(spec)))

        attr_and_rest = attr_name_and_rest_match.groups()

        target_and_name_match = re.search(
            r'^(\w+) +as +(\w+)$', attr_and_rest[1])

        if target_and_name_match:
            attr_target_and_name = (
                attr_and_rest[0:1] + target_and_name_match.groups())
        else:
            attr_target_and_name = attr_and_rest + attr_and_rest[0:1]

        for kwd in attr_target_and_name:
            if re.search(r'^\d', kwd):
                msg = (
                    f'Keyword {repr(kwd)} in spec starts with a digit, so it '
                    'is not valid as a Python keyword.')
                raise ValueError(msg)

        for kwd in attr_target_and_name:
            if ' ' in kwd:
                raise ValueError(
                    self.SPEC_DOES_NOT_FOLLOW_PATTERN_FMT.format(repr(spec)))

        self.attr_name, self.target_name, self.name = attr_target_and_name
        self.with_setter = with_setter
