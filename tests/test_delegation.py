from delegation import Delegation

import pytest


def test_rejects_spec_without_to_clause():
    with pytest.raises(ValueError, match=r'\b[Ss]pec\b'):
        Delegation("foo")


def test_rejects_spec_with_leading_digits_in_keywords():
    with pytest.raises(ValueError, match=r'\b[Ss]pec\b'):
        Delegation("foo to 2bar")

    with pytest.raises(ValueError, match=r'\b[Ss]pec\b'):
        Delegation("3foo to bar")


def test_rejects_spec_with_extra_word():
    with pytest.raises(ValueError, match=r'\b[Ss]pec\b'):
        Delegation("foo to bar xyz")

    with pytest.raises(ValueError, match=r'\b[Ss]pec\b'):
        Delegation("foo to bar as baz xyz")

    with pytest.raises(ValueError, match=r'\b[Ss]pec\b'):
        Delegation("foo xyz to bar")


def test_rejects_spec_with_invalid_char():
    with pytest.raises(ValueError, match=r'\b[Ss]pec\b'):
        Delegation("foo! to bar")


def test_parses_valid_minimal_spec():
    deleg = Delegation("foo to bar")
    assert (deleg.attr_name, deleg.target_name) == ('foo', 'bar')


def test_parses_valid_spec_with_name():
    deleg = Delegation("foo to bar as baz")
    attr_target_name = (deleg.attr_name, deleg.target_name, deleg.name)
    assert attr_target_name == ('foo', 'bar', 'baz')
