# Activity 6.2 - Reservation System (Programming Exercise 3 & Unit Tests)

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

## Static Analysis

```bash
flake8 hotel.py customer.py reservation.py
pylint hotel.py customer.py reservation.py
```
