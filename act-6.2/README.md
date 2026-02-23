# Activity 6.2 - Reservation System

[![CI](https://github.com/ArtemioPadilla/mna-qa/actions/workflows/ci.yml/badge.svg)](https://github.com/ArtemioPadilla/mna-qa/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-blue)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
![Pylint](https://img.shields.io/badge/pylint-10.00%2F10-brightgreen)
![Flake8](https://img.shields.io/badge/flake8-0%20errors-brightgreen)

QA course assignment: implement a hotel reservation system in Python with three classes, JSON persistence, and comprehensive unit tests.

## Requirements

| Req | Description |
|-----|-------------|
| R1 | Three classes: Hotel, Customer, Reservation |
| R2 | Persistent behaviors stored in JSON files |
| R3 | Unit tests using Python's `unittest` module |
| R4 | At least 85% line coverage |
| R5 | Handle invalid data gracefully (errors to console, continue execution) |
| R6 | PEP-8 compliant |
| R7 | Zero warnings from flake8 and pylint |

## Classes

**Hotel** (`hotel.py`): create, delete, display, modify, reserve_room, cancel_reservation

**Customer** (`customer.py`): create, delete, display, modify

**Reservation** (`reservation.py`): create (links customer + hotel), cancel

## How to Run

```bash
# Run all unit tests
python -m unittest discover -v

# Run coverage
coverage run -m unittest discover && coverage report -m
```

## Tests

62 tests across three files:

- `test_hotel.py` — 28 tests (create, delete, display, modify, reserve, cancel, persistence)
- `test_customer.py` — 20 tests (create, delete, display, modify, persistence)
- `test_reservation.py` — 14 tests (create, cancel, persistence, cross-class validation)

Includes **19+ negative test cases**: duplicate IDs, invalid inputs, non-existent records, no rooms available, corrupted JSON, invalid emails.

## Static Analysis

```bash
flake8 hotel.py customer.py reservation.py
pylint hotel.py customer.py reservation.py
```

## Sample Data

The `data/` directory contains example JSON files showing the persistence format:

- `data/hotels.json` — 3 sample hotels
- `data/customers.json` — 3 sample customers
- `data/reservations.json` — 3 sample reservations

## Results

| Metric | Result |
|--------|--------|
| flake8 | 0 errors |
| pylint | 10.00/10 |
| Tests | 62 passed |
| Coverage | 100% (hotel.py, customer.py, reservation.py) |
