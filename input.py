from fractions import Fraction
from decimal import Decimal


class CalcEngine:
    def __init__(self):
        self.current = Fraction(0)      # operando actual
        self.stored = None             # operando previo
        self.pending = None            # operador pendiente: '+','-','*','/'
        self.reset_next = False        # indica que el próximo dígito reinicia la entrada

    def process_digit(self, d: str):
        if self.reset_next:
            self.current = Fraction(0)
            self.reset_next = False
        # concatenar dígitos y punto decimal (usar decimal.Decimal o manejar strings)

    def process_operator(self, op: str):
        if self.pending is not None:
            self._apply_pending()
        else:
            self.stored = self.current
        self.pending = op
        self.reset_next = True        # la siguiente entrada empieza un nuevo número

    def process_equals(self):
        if self.pending is not None:
            self._apply_pending()
            self.pending = None
        self.reset_next = True

    def _apply_pending(self):
        if self.pending == '+':
            self.stored += self.current
        elif self.pending == '-':
            self.stored -= self.current
        elif self.pending == '*':
            self.stored *= self.current
        elif self.pending == '/':
            # gestión de división por cero
            self.stored /= self.current
        self.current = self.stored
