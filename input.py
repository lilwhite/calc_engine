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