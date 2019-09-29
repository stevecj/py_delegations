from delegation import Delegation

import pytest


def test_rejects_spec_without_to():
    with pytest.raises(ValueError, match='" to "'):
        Delegation("foo")


def test_rejects_spec_with_too_many_tos():
    with pytest.raises(ValueError, match='" to "'):
        Delegation("foo to bar to baz")


def test_rejects_spec_with_leading_digits_in_keywords():
    with pytest.raises(ValueError, match='[Dd]igit'):
        Delegation("foo to 2bar")

    with pytest.raises(ValueError, match='[Dd]igit'):
        Delegation("3foo to bar")


def test_rejects_spec_with_spaces_in_keywords():
    with pytest.raises(ValueError, match='[Ss]pace'):
        Delegation("foo to bar baz")

    with pytest.raises(ValueError, match='[Ss]pace'):
        Delegation("foo baz to bar")


def test_rejects_spec_with_invalid_char():
    with pytest.raises(ValueError, match='[Cc]har'):
        Delegation("foo! to bar")


def test_parses_valid_minimal_spec():
    deleg = Delegation("foo to bar")
    assert (deleg.attr_name, deleg.target_name) == ('foo', 'bar')
