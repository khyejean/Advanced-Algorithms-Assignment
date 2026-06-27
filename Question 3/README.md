# Question 3: Concurrent Process

## Overview

This project answers Question 3 of the Advanced Algorithm assignment. It compares factorial calculation using multithreading and without multithreading.

## Main Requirements Covered

- Function to calculate factorial
- Big-O derivation for factorial
- Three separate threads:
  - One thread calculates 50!
  - One thread calculates 100!
  - One thread calculates 200!
- Nanosecond timing using `time.perf_counter_ns()`
- 10 rounds of testing for multithreading
- 10 rounds of testing without multithreading
- Average time calculation
- Comparison and analysis
- Clean menu-driven output

## Program Menu

The Python program does not include the first two theory questions as menu options. It focuses on the practical experiment outputs:

1. Show factorial Big-O derivation
2. Run multithreading experiment
3. Run non-multithreading experiment
4. Run full comparison experiment
5. Exit

## Folder Structure

```text
Question 3
│
├── Question_3.py
├── README.md
├── sample_output.txt
│
└── src/
    ├── __init__.py
    ├── analysis_text.py
    ├── cli.py
    ├── experiments.py
    ├── factorial.py
    ├── formatting.py
    └── models.py
```

## How to Run

```bash
python Question_3.py
```

Run the command from the project root folder.

## Recommended Python Version

Python 3.10 or later.

No external packages are required.
