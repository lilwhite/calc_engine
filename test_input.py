import pytest

from input import InputBuffer, capture_keypress, read_input_line

@ pytest.fixture
def buffer():
    """Fixture that returns a fresh InputBuffer instance for each test."""
    return InputBuffer()


def test_append_single_character(buffer):
    buffer.append('a')
    assert buffer.get_contents() == 'a'


def test_append_invalid_string_raises(buffer):
    with pytest.raises(ValueError):
        buffer.append('ab')
    with pytest.raises(ValueError):
        buffer.append('')


def test_get_contents_accumulates(buffer):
    for ch in 'Hello':
        buffer.append(ch)
    assert buffer.get_contents() == 'Hello'


def test_clear_empties_buffer(buffer):
    for ch in 'Test':
        buffer.append(ch)
    buffer.clear()
    assert buffer.get_contents() == ''


def test_capture_keypress(buffer):
    capture_keypress(buffer, 'x')
    assert buffer.get_contents() == 'x'


def test_read_input_line_no_prompt(monkeypatch):
    # Simulate input() without prompt
    monkeypatch.setattr('builtins.input', lambda: 'user input')
    result = read_input_line()
    assert result == 'user input'


def test_read_input_line_with_prompt(monkeypatch):
    # Simulate input() with a prompt
    prompt = 'Enter: '
    captured = {'prompt': None}

    def fake_input(p=None):
        captured['prompt'] = p
        return 'prompted input'

    monkeypatch.setattr('builtins.input', fake_input)
    result = read_input_line(prompt)

    assert captured['prompt'] == prompt
    assert result == 'prompted input'