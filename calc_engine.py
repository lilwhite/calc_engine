from fractions import Fraction

class CalcEngine:
    """
    Calculator engine supporting multi-digit, decimal inputs, operator precedence, and basic error handling.
    """
    MAX_ENTRY_LENGTH = 16  # maximum characters in entry buffer

    def __init__(self):
        # Initialize calculator state
        self.current = Fraction(0)      # current operand
        self.stored = None             # stored operand (unused with full expression)
        self.pending = None            # last operator pressed
        self.reset_next = False        # flag: next digit resets entry
        self._entry_str = '0'          # input buffer string
        self._tokens = []              # list of tokens (Fraction or operator str)
        self.error = False             # error flag

    def process_digit(self, d: str):
        """
        Handle digit or decimal point input:
        - If reset_next, start fresh entry.
        - Append digit or decimal point if valid and within length limits.
        - Update current from entry buffer.
        """
        if self.reset_next:
            self._entry_str = ''
            self.reset_next = False
            self.error = False

        # enforce max length
        if len(self._entry_str) >= self.MAX_ENTRY_LENGTH:
            return

        if d == '.':
            if '.' not in self._entry_str:
                self._entry_str = self._entry_str or '0'
                self._entry_str += '.'
        elif d.isdigit():
            if self._entry_str == '0':
                self._entry_str = d
            else:
                self._entry_str += d
        else:
            return  # ignore invalid input

        try:
            self.current = Fraction(self._entry_str)
        except (ValueError, ZeroDivisionError):
            self.current = Fraction(0)
            self.error = True

    def process_operator(self, op: str):
        """
        Handle operator input:
        - Append current to tokens, then operator.
        - Flag reset for next entry.
        """
        if self.error:
            return
        # append current value as token
        self._tokens.append(self.current)
        # append operator
        self._tokens.append(op)
        self.reset_next = True

    def process_equals(self):
        """
        Evaluate the full expression with operator precedence and update current.
        """
        if self.error:
            return
        self._tokens.append(self.current)
        try:
            result = self._evaluate_tokens()
            self.current = result
            # reset tokens and entry buffer
            self._tokens.clear()
            self._entry_str = str(self.current)
        except ZeroDivisionError:
            self.current = Fraction(0)
            self.error = True
            self._tokens.clear()
            self._entry_str = '0'
        self.reset_next = True

    def process_clear(self):
        """Clear all state."""
        self.__init__()

    def process_clear_entry(self):
        """Clear only the entry buffer."""
        self.current = Fraction(0)
        self._entry_str = '0'
        self.reset_next = True
        self.error = False

    def process_backspace(self):
        """Remove last char from entry buffer."""
        if self.reset_next or self.error:
            self.process_clear_entry()
            return
        if len(self._entry_str) > 1:
            self._entry_str = self._entry_str[:-1]
        else:
            self._entry_str = '0'
        try:
            self.current = Fraction(self._entry_str)
        except ValueError:
            self.current = Fraction(0)
            self.error = True

    def process_plus_minus(self):
        """Toggle sign of current entry."""
        if self.error:
            return
        self.current = -self.current
        self._entry_str = str(self.current)
        self.reset_next = True

    def _evaluate_tokens(self):
        """
        Convert infix tokens to RPN with shunting yard, then evaluate.
        """
        # shunting-yard algorithm
        prec = {'+': 1, '-': 1, '*': 2, '/': 2}
        output_queue = []
        op_stack = []
        for token in self._tokens:
            if isinstance(token, Fraction):
                output_queue.append(token)
            else:
                while op_stack and prec[op_stack[-1]] >= prec[token]:
                    output_queue.append(op_stack.pop())
                op_stack.append(token)
        while op_stack:
            output_queue.append(op_stack.pop())
        # evaluate RPN
        stack = []
        for token in output_queue:
            if isinstance(token, Fraction):
                stack.append(token)
            else:
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    res = a + b
                elif token == '-':
                    res = a - b
                elif token == '*':
                    res = a * b
                elif token == '/':
                    res = a / b
                stack.append(res)
        return stack[0]

# Simple CLI UI stub
if __name__ == '__main__':
    engine = CalcEngine()
    print("CalcEngine CLI. Enter digits, operators (+ - * /), '=' to evaluate, 'c' to clear, 'q' to quit.")
    while True:
        key = input(f"[{engine._entry_str}] > ")
        if key == 'q':
            break
        elif key == 'c':
            engine.process_clear()
        elif key == 'ce':
            engine.process_clear_entry()
        elif key == 'bs':
            engine.process_backspace()
        elif key == '+/-':
            engine.process_plus_minus()
        elif key in '+-*/':
            engine.process_operator(key)
        elif key == '=':
            engine.process_equals()
        elif key.isdigit() or key == '.':
            engine.process_digit(key)
        else:
            print("Unknown input")
        if engine.error:
            print("Error")
        else:
            print(engine.current)
