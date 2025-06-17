from typing import Optional

class InputBuffer:
    """
    Buffers individual character inputs before submitting the full line.
    """
    def __init__(self) -> None:
        # Internal list to store buffered characters
        self._buffer = []  # List[str]

    def append(self, char: str) -> None:
        """Adds a single character to the input buffer."""
        if len(char) != 1:
            raise ValueError("Only a single character is allowed.")
        self._buffer.append(char)

    def get_contents(self) -> str:
        """Returns the complete accumulated string."""
        return ''.join(self._buffer)

    def clear(self) -> None:
        """Clears the input buffer."""
        self._buffer.clear()


def capture_keypress(buffer: InputBuffer, char: str) -> None:
    """Convenience function to add a character to the buffer."""
    buffer.append(char)


def read_input_line(prompt: Optional[str] = None) -> str:
    """
    Reads a full line from standard input. For testing purposes, the input() function
    can be patched.
    """
    if prompt is not None:
        return input(prompt)
    return input()

# Pytest tests
import pytest

@ pytest.fixture

def input_buffer() -> InputBuffer:
    """Fixture for a fresh InputBuffer instance."""
    return InputBuffer()


def test_append_and_get(input_buffer):
    capture_keypress(input_buffer, '1')
    capture_keypress(input_buffer, '+')
    capture_keypress(input_buffer, '2')
    assert input_buffer.get_contents() == '1+2'


def test_clear_buffer(input_buffer):
    input_buffer.append('a')
    input_buffer.clear()
    assert input_buffer.get_contents() == ''


def test_append_invalid_character(input_buffer):
    with pytest.raises(ValueError):
        input_buffer.append('ab')


def test_read_line_without_prompt(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: '123+456')
    line = read_input_line()
    assert line == '123+456'


def test_read_line_with_prompt(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda prompt=None: 'sin(90)')
    line = read_input_line('Expr> ')
    assert line == 'sin(90)'
