import pytest
from fractions import Fraction

from input import CalcEngine

@ pytest.fixture
def engine():
    return CalcEngine()


def test_initial_state(engine):
    assert engine.current == Fraction(0)
    assert engine.stored is None
    assert engine.pending is None
    assert engine.reset_next is False


def test_addition(engine):
    # 2 + 3 = 5
    engine.current = Fraction(2)
    engine.process_operator('+')
    engine.current = Fraction(3)
    engine.process_equals()
    assert engine.current == Fraction(5)
    assert engine.pending is None


def test_subtraction(engine):
    # 5 - 2 = 3
    engine.current = Fraction(5)
    engine.process_operator('-')
    engine.current = Fraction(2)
    engine.process_equals()
    assert engine.current == Fraction(3)


def test_multiplication(engine):
    # 4 * 3 = 12
    engine.current = Fraction(4)
    engine.process_operator('*')
    engine.current = Fraction(3)
    engine.process_equals()
    assert engine.current == Fraction(12)


def test_division(engine):
    # 10 / 2 = 5
    engine.current = Fraction(10)
    engine.process_operator('/')
    engine.current = Fraction(2)
    engine.process_equals()
    assert engine.current == Fraction(5)


def test_division_by_zero(engine):
    # Division by zero should raise ZeroDivisionError
    engine.current = Fraction(10)
    engine.process_operator('/')
    engine.current = Fraction(0)
    with pytest.raises(ZeroDivisionError):
        engine.process_equals()


def test_chain_operations(engine):
    # 1 + 2 * 3 = (1 + 2) * 3 = 9 (left-to-right without precedence)
    engine.current = Fraction(1)
    engine.process_operator('+')
    engine.current = Fraction(2)
    engine.process_operator('*')
    engine.current = Fraction(3)
    engine.process_equals()
    assert engine.current == Fraction(9)


def test_reset_next_flag(engine):
    # After equals, reset_next should be True
    engine.current = Fraction(7)
    engine.process_equals()
    assert engine.reset_next is True


def test_process_digit_resets_current(engine):
    # Simulate entering a digit after reset_next
    engine.current = Fraction(5)
    engine.reset_next = True
    engine.process_digit('3')
    # Assuming process_digit resets current and sets to the new digit
    assert engine.current == Fraction(3)
