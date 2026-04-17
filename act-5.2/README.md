# Activity 5.2 - Compute Sales (Programming Exercise 2 & Static Analysis)

QA course assignment: build a Python CLI program that computes total sales from JSON files, then verify code quality with flake8 and pylint.

## Requirements

| Req | Description |
|-----|-------------|
| R1 | CLI program receiving two JSON files as arguments |
| R2 | Compute total cost for all sales; output to screen and `SalesResults.txt` |
| R3 | Handle invalid data gracefully (log errors to console, continue execution) |
| R4 | Program name: `computeSales.py` |
| R5 | Invocation: `python computeSales.py priceCatalogue.json salesRecord.json` |
| R6 | Support hundreds to thousands of items |
| R7 | Print elapsed execution time (screen + results file) |
| R8 | PEP-8 compliant |

## How to Run

```bash
# Run with test case 1
python computeSales.py "A5.2 Archivos de Apoyo/TC1/TC1.ProductList.json" "A5.2 Archivos de Apoyo/TC1/TC1.Sales.json"

# Run with test case 2
python computeSales.py "A5.2 Archivos de Apoyo/TC1/TC1.ProductList.json" "A5.2 Archivos de Apoyo/TC2/TC2.Sales.json"

# Run with test case 3
python computeSales.py "A5.2 Archivos de Apoyo/TC1/TC1.ProductList.json" "A5.2 Archivos de Apoyo/TC3/TC3.Sales.json"
```

## Tests

```bash
# Run all tests
pytest test_computeSales.py -v
```

The test suite (`test_computeSales.py`) covers:

- **Unit tests** -- catalogue building, sales computation, grand total calculation
- **Integration tests** -- verifies TC1/TC2/TC3 grand totals match expected values
- **CLI tests** -- runs the program as a subprocess, checks output and exit codes
- **Error handling** -- negative quantities flagged, unknown products (Elotes, Frijoles) detected
- **Static analysis** -- flake8 and pylint pass with zero errors

## Static Analysis

```bash
# flake8
flake8 computeSales.py

# pylint
pylint computeSales.py
```

## Test Cases & Expected Totals

| Test Case | Product Catalogue | Sales File | Expected Total |
|-----------|-------------------|------------|----------------|
| TC1 | TC1.ProductList.json | TC1.Sales.json | 2,481.86 |
| TC2 | TC1.ProductList.json | TC2.Sales.json | 166,568.23 |
| TC3 | TC1.ProductList.json | TC3.Sales.json | 165,235.37 |

**Notes on invalid data in test files:**
- TC2 & TC3 contain negative quantities (should be flagged as errors)
- TC3 contains products not in the catalogue ("Elotes", "Frijoles")

## Grading Rubric (100 pts)

| Criteria | Full (20 pts) | Partial (10 pts) | Fail (1 pt) |
|----------|---------------|-------------------|--------------|
| Pylint / PEP-8 errors | 0 errors | Up to 3 errors | More than 3 |
| Flake8 errors | 0 errors | Up to 3 errors | More than 3 |

| Criteria | Full (60 pts) | Partial (30 pts) | Fail (1 pt) |
|----------|---------------|-------------------|--------------|
| Test cases passing | 3 correct | 2 correct | 1 or fewer |
