import pytest
from fractions import Fraction

from calc_engine import CalcEngine

@ pytest.fixture
def engine():
    return CalcEngine()

# Basic state tests

def test_initial_state(engine):
    assert engine.current == Fraction(0)
    assert engine._entry_str == '0'
    assert engine._tokens == []
    assert engine.error is False

# Digit and decimal input tests

def test_multi_digit_input(engine):
    for d in ['1', '2', '3']:
        engine.process_digit(d)
    assert engine._entry_str == '123'
    assert engine.current == Fraction(123)


def test_decimal_input(engine):
    for d in ['0', '.', '5', '2']:
        engine.process_digit(d)
    assert engine._entry_str == '0.52'
    assert engine.current == Fraction('0.52')


def test_max_length_limit(engine):
    for _ in range(engine.MAX_ENTRY_LENGTH + 5):
        engine.process_digit('9')
    assert len(engine._entry_str) == engine.MAX_ENTRY_LENGTH
    # value corresponds to repeated '9'
    assert engine.current == Fraction(int('9'*engine.MAX_ENTRY_LENGTH))

# Operator precedence and evaluation

def test_operator_precedence(engine):
    # 1 + 2 * 3 = 7
    for ch in '1': engine.process_digit(ch)
    engine.process_operator('+')
    for ch in '2': engine.process_digit(ch)
    engine.process_operator('*')
    for ch in '3': engine.process_digit(ch)
    engine.process_equals()
    assert engine.current == Fraction(7)


def test_left_to_right_same_precedence(engine):
    # 6 / 3 * 2 = (6/3)*2 = 4
    for ch in '6': engine.process_digit(ch)
    engine.process_operator('/')
    for ch in '3': engine.process_digit(ch)
    engine.process_operator('*')
    for ch in '2': engine.process_digit(ch)
    engine.process_equals()
    assert engine.current == Fraction(4)

# Clear functions

def test_clear_entry(engine):
    for ch in '45': engine.process_digit(ch)
    engine.process_clear_entry()
    assert engine._entry_str == '0'
    assert engine.current == Fraction(0)


def test_clear_all(engine):
    engine.process_digit('9')
    engine.process_operator('+')
    engine.process_digit('1')
    engine.process_clear()
    assert engine._entry_str == '0'
    assert engine._tokens == []
    assert engine.current == Fraction(0)
    assert engine.error is False

# Backspace

def test_backspace(engine):
    for ch in '123': engine.process_digit(ch)
    engine.process_backspace()
    assert engine._entry_str == '12'
    assert engine.current == Fraction(12)


def test_backspace_to_zero(engine):
    engine.process_digit('5')
    engine.process_backspace()
    assert engine._entry_str == '0'
    assert engine.current == Fraction(0)

# Plus-minus toggle

def test_plus_minus_toggle(engine):
    for ch in '42': engine.process_digit(ch)
    engine.process_plus_minus()
    assert engine.current == Fraction(-42)
    assert engine._entry_str.startswith('-')

# Division by zero error

def test_division_by_zero_sets_error(engine):
    # simulate expression 5 / 0 = error
    engine.process_digit('5')
    engine.process_operator('/')
    engine.process_digit('0')
    engine.process_equals()
    assert engine.error is True
    assert engine.current == Fraction(0)

# After error, digit resets engine

def test_digit_after_error_resets(engine):
    engine.process_digit('5')
    engine.process_operator('/')
    engine.process_digit('0')
    engine.process_equals()
    # now error True
    engine.process_digit('7')
    assert engine.error is False
    assert engine._entry_str == '7'
    assert engine.current == Fraction(7)

if __name__ == '__main__':
    pytest.main()
