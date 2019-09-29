from delegation import Delegation, SpecValueError

import pytest


def test_rejects_spec_without_to_clause():
    with pytest.raises(SpecValueError):
        Delegation("foo")


def test_rejects_spec_with_leading_digit_in_keyword():
    specs = (
        'foo to 2bar',
        '3foo to bar',
        )

    for spec in specs:
        with pytest.raises(SpecValueError):
            Delegation(spec)


def test_rejects_spec_with_extra_word():
    specs = (
        'foo to bar xyz',
        'foo to bar as baz xyz',
        'foo xyz to bar',
        )

    for spec in specs:
        with pytest.raises(SpecValueError):
            Delegation(spec)


def test_rejects_spec_with_invalid_char():
    with pytest.raises(SpecValueError):
        Delegation("foo! to bar")


def test_parses_valid_minimal_spec():
    deleg = Delegation("foo to bar")
    attr_target = (deleg.attr_name, deleg.target_name)
    assert attr_target == ('foo', 'bar')


def test_parses_valid_spec_with_name():
    deleg = Delegation("foo to bar as baz")
    attr_target_name = (deleg.attr_name, deleg.target_name, deleg.name)
    assert attr_target_name == ('foo', 'bar', 'baz')
