# Question 2: Divide and Conquer Algorithm

## Overview

This project implements a Divide and Conquer system for sorting and searching online shopping customer transaction data.

## Algorithms Implemented

1. Merge Sort
   - Recursive implementation
   - Clearly separates Divide, Conquer, and Combine steps
   - Sorts transactions by Transaction ID
   - Can also sort by other attributes as an extra feature

2. Binary Search
   - Recursive implementation
   - Searches transactions by Transaction ID
   - Requires transactions to be sorted by Transaction ID

3. Linear Search
   - Used for comparison with Binary Search
   - Works even when data is unsorted

## Features

### Mandatory Features

- Display all transactions
- Sort transactions using Merge Sort
- Search transaction using Binary Search
- Search transaction using Linear Search
- Display array before sorting
- Display array after sorting
- Show recursive Merge Sort calls
- Search for existing and non-existing transactions
- Measure execution time for performance comparison

### Extra Features Implemented

- Insert transaction dynamically
- Sort by different attributes such as amount, customer name, product name, and date
- Count recursive calls made during Merge Sort
- Display time complexity analysis in table format
- Formatted CLI output for better readability

## Folder Structure

```text
Question 2
│
├── Question_2.py
├── README.md
│
├── data/
│   └── sample_transactions.csv
│
└── src/
    ├── __init__.py
    ├── cli.py
    ├── formatting.py
    ├── merge_sort.py
    ├── models.py
    ├── performance.py
    ├── search.py
    └── transaction_system.py
```

## How to Run

```bash
python Question_2.py
```

Run the command from the project root folder.

## Recommended Python Version

Python 3.10 or later.

No external packages are required.
