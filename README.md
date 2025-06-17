# CalcEngine: CLI Calculator in Python

A lightweight, terminal-based calculator engine with support for:

* **Multi-digit and decimal input**
* **Operator precedence** (`*` and `/` before `+` and `-`)
* **Clear**, **Clear Entry**, and **Backspace** operations
* **Plus/Minus** toggle for changing sign
* **Error handling** (e.g., division by zero)
* **ASCII startup animation** and **spinner** on evaluation

---

## Table of Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Usage](#usage)

   * [Interactive CLI](#interactive-cli)
   * [Programmatic API](#programmatic-api)
4. [Key Bindings](#key-bindings)
5. [Testing](#testing)
6. [Project Structure](#project-structure)
7. [Contributing](#contributing)
8. [License](#license)

---

## Requirements

* Python 3.6 or higher
* No external dependencies (only standard library modules `fractions`, `itertools`, `time`, `sys`, `os`)

---

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/calcmodule.git
   cd calcmodule
   ```
2. (Optional) Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate    # Windows
   ```
3. Install development requirements (for tests):

   ```bash
   pip install pytest
   ```

---

## Usage

### Interactive CLI

Run the calculator in your terminal:

```bash
python calc_engine.py
```

Upon start, you'll see a brief ASCII animation banner before the prompt appears. Enter keys as follows (see [Key Bindings](#key-bindings)):

```text
[0] > 12         # entering digits 1 and 2
12
[12] > +         # press + to add
12
[12] > 3         # entering 3
3
[3] > =         # evaluate
 Calculating /-\\|   # spinner animation
15
```

The prompt always displays the current entry buffer in brackets. Results and errors appear on subsequent lines.

### Programmatic API

Import and use `CalcEngine` in your Python scripts:

```python
from calc_engine import CalcEngine
from fractions import Fraction

engine = CalcEngine()
# Input 6/3*2 programmatically:
for ch in '6': engine.process_digit(ch)
engine.process_operator('/')
for ch in '3': engine.process_digit(ch)
engine.process_operator('*')
for ch in '2': engine.process_digit(ch)
engine.process_equals()
print(engine.current)  # prints Fraction(4, 1)
```

---

## Key Bindings

| Input     | Description                   |
| --------- | ----------------------------- |
| `0-9`     | Enter digit                   |
| `.`       | Decimal point                 |
| `+,-,*,/` | Arithmetic operators          |
| `=`       | Evaluate current expression   |
| `c`       | Clear all state               |
| `ce`      | Clear current entry only      |
| `bs`      | Backspace (delete last digit) |
| `+/-`     | Toggle sign of entry          |
| `q`       | Quit the CLI                  |

---

## Testing

Automated tests are written with [pytest](https://docs.pytest.org/).

Run all tests:

```bash
pytest
```

All core functionality, edge cases, and CLI utility methods are covered.

---

## Project Structure

```
├── calc_engine.py    # Main calculator engine and CLI stub
├── README.md         # This documentation file
├── LICENSE           # MIT License
├── tests/
│   └── test_calc_engine.py  # pytest test suite
└── venv/             # (optional) virtualenv directory
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open a Pull Request

Please ensure all new features include appropriate tests and documentation.

---

## Author

**Mario Blanco**
Email: [mario.blanco85@outlook.es](mailto:mario.blanco85@outlook.es)
GitHub: [lilwhite](https://github.com/lilwhite)

## License

This project is licensed under the [MIT License](./LICENSE).
