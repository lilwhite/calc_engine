from fractions import Fraction
from decimal import Decimal


class CalcEngine:
    def __init__(self):
        self.current = Fraction(0)      # operando actual
        self.stored = None              # operando previo
        self.pending = None             # operador pendiente: '+','-','*','/'
        self.reset_next = False         # indica que el próximo dígito reinicia la entrada
        self._entry_str = '0'           # añadimos un string para construir el número dígito a dígito
    
    def process_digit(self, d: str):
        if self.reset_next:
            # comenzamos nueva entrada
            self._entry_str = '0'
            self.reset_next = False
        # si es el primer 0 y viene un dígito distinto de '.', lo reemplazamos
        if self._entry_str == '0' and d != '.':
            self._entry_str = d
        else:
            self._entry_str += d
        # convertimos la cadena a Fraction (sin decimales por ahora)
        # para soportar decimales habría que parsear como Decimal
        self.current = Fraction(int(self._entry_str))
        
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
