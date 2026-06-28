# Question 1: Hashing - Pharmacy Inventory System

## Overview

This project implements a Hash Table using Linear Probing and applies it to a local Pharmacy Inventory System.

## Features

- Reusable generic `LinearProbingHashTable`
- Open addressing with linear probing
- Lazy deletion using a deleted marker
- Automatic resizing when load factor becomes high
- `Medicine` entity class
- Predefined sample medicine records with expiry dates loaded from CSV
- Command-line inventory system
- Display inventory records
- Display hash table buckets
- Insert medicine
- Search medicine
- Edit medicine stock quantity or price
- Delete medicine
- Display hash table statistics
- Performance comparison between Hash Table search and one-dimensional array search
- Clean, modular, well-commented Python code

## Folder Structure

```text
Question 1/
│
├── Question_1.py
├── README.md
│
├── data/
│   └── sample_medicines.csv
│
└── src/
    ├── __init__.py
    ├── cli.py
    ├── formatting.py
    ├── hash_table.py
    ├── inventory.py
    ├── models.py
    └── performance.py
```

## How to Run

Open the project folder in PyCharm or another Python IDE.

Then run:

```bash
python Question_1.py
```

## Main Menu

```text
1. Display inventory records
2. Display hash table buckets
3. Insert new medicine
4. Search medicine by ID
5. Edit medicine stock or price
6. Delete medicine
7. View hash table statistics
8. Run performance comparison
9. Exit
```

## Python Version

Recommended Python version: Python 3.10 or later.

No external packages are required.

## Expiry Date

Each medicine record includes an `expiry_date` field in `YYYY-MM-DD` format. This improves the pharmacy inventory system because medicine expiry dates are important for safe stock management.
