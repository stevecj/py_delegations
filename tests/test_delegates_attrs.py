from delegation import DelegatesAttrs


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


def test_delegated_value_get():
    Wrapper = make_wrapper_class("""
    delegate('color to inner_obj')
""")
    wrapper = Wrapper(Inner())

    assert wrapper.color == 'purple'


def test_delegated_method_call():
    Wrapper = make_wrapper_class("""
    delegate('get_hello to inner_obj')
""")
    wrapper = Wrapper(Inner())

    assert wrapper.get_hello() == 'Hello from inner subject!'
