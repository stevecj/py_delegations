from delegation import DelegatesAttrs  # noqa: F401

import pytest


class Inner:
    color = 'purple'

    def get_hello(self):
        return 'Hello from inner subject!'


def make_wrapper_class(body_lines):
    code = f"""
class Wrapper(DelegatesAttrs):
{body_lines}

    def __init__(self, inner_obj):
        self.inner_obj = inner_obj
"""
    exec(code)
    return eval('Wrapper')


def test_delegates_value_get():
    Wrapper = make_wrapper_class("""
    delegate('color to inner_obj')
""")
    wrapper = Wrapper(Inner())

    assert wrapper.color == 'purple'


def test_delegates_method_call():
    Wrapper = make_wrapper_class("""
    delegate('get_hello to inner_obj')
""")
    wrapper = Wrapper(Inner())

    assert wrapper.get_hello() == 'Hello from inner subject!'


def test_makes_explicitly_named_delegation():
    Wrapper = make_wrapper_class("""
    delegate('get_hello to inner_obj as get_hi')
""")
    wrapper = Wrapper(Inner())

    assert wrapper.get_hi() == 'Hello from inner subject!'


def test_does_not_add_setter_by_default():
    Wrapper = make_wrapper_class("""
    delegate('color to inner_obj')
""")
    wrapper = Wrapper(Inner())

    with pytest.raises(AttributeError):
        wrapper.color = 'green'


def test_delegates_assignment_when_setter_specified():
    Wrapper = make_wrapper_class("""
    delegate('color to inner_obj', setter=True)
""")
    inner = Inner()
    wrapper = Wrapper(inner)

    wrapper.color = 'green'
    assert inner.color == 'green'
