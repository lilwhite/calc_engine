from fractions import Fraction

class CalcEngine:
    def __init__(self):
        self.current = Fraction(0)      # operando actual
        self.stored = None             # operando previo
        self.pending = None            # operador pendiente: '+','-','*','/'
        self.reset_next = False        # indica que el próximo dígito reinicia la entrada
        # buffer de entrada como string para manejar múltiples dígitos y decimales
        self._entry_str = '0'

    def process_digit(self, d: str):
        """
        Procesa un dígito o punto decimal:
        - Si reset_next es True, reinicia la entrada.
        - Construye un string con dígitos y un posible punto único.
        - Actualiza current como Fraction del string resultante.
        """
        # Si toca reiniciar, comenzamos nueva entrada
        if self.reset_next:
            self._entry_str = ''
            self.reset_next = False
        # Manejo de punto decimal
        if d == '.':
            if '.' not in self._entry_str:
                # si estaba vacío, ante '.', ponemos '0.'
                if self._entry_str == '':
                    self._entry_str = '0.'
                else:
                    self._entry_str += '.'
        else:
            # dígito numérico
            # evito ceros a la izquierda
            if self._entry_str == '0':
                self._entry_str = d
            else:
                self._entry_str += d
        # Convertir la cadena en Fracción (Fraction acepta strings con decimales)
        try:
            self.current = Fraction(self._entry_str)
        except ValueError:
            # cadena no convertible (p.ej. solo '.'), dejamos current en 0
            self.current = Fraction(0)

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
            # gestión de división por cero natural de Fraction
            self.stored /= self.current
        self.current = self.stored
        # tras operación, preparamos buffer para seguir concatenando si es necesario
        self._entry_str = str(self.current)
