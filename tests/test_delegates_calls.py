from delegation import DelegatesAttrs


class InnerSubject:
    def get_hello(self):
        return 'Hello from inner subject!'


class WrapperSubject(DelegatesAttrs):
    delegate('get_hello to inner_obj')

    def __init__(self, inner_obj):
        self.inner_obj = inner_obj


def test_something():
    inner_subject = InnerSubject()
    wrapper_subject = WrapperSubject(inner_subject)

    assert wrapper_subject.get_hello() == 'Hello from inner subject!'
