# Model code

- `nvda_model.py`: a rebuild of Aswath Damodaran's valuation spreadsheet in Python. Running it reproduces his Anthropic valuation (equity of $1,450,478 million) as a check.
- `nvda_run.py`: NVIDIA's inputs, the value grids, the reverse check (what growth the price implies) and the sensitivities used in the piece.
- `three_year_check.py`: the 3 year check in Part 5.
- `engine.js`: the same math in JavaScript, used by the calculator on the page.

The workbook one folder up holds the same valuation in Damodaran's own spreadsheet layout, with every input on the Input sheet.
