# Advanced Algorithm Assignment

## Overview

This repository contains the complete Python source code for my Advanced Algorithms assignment. The assignment consists of three main programming questions, each focusing on a different algorithmic concept and practical implementation.

The project demonstrates the use of data structures, divide and conquer algorithms, searching techniques, sorting techniques, performance comparison, recursion and concurrent processing. Each question is organized into its own folder with source code and supporting files.

## Assignment Questions

### Question 1: Hashing

Question 1 implements a Hash Table using Linear Probing as the collision-resolution technique. The hash table is applied to a simple local Pharmacy Inventory System.

Main concepts covered:

* Hash Table
* Linear Probing
* Open Addressing
* Collision Handling
* Pharmacy Inventory Management System
* Hash Table Search vs. One-Dimensional Array Search
* Performance Comparison

Main features:

* Medicine entity class
* Predefined medicine records
* Display inventory records
* Insert medicine records
* Search medicine records
* Edit and delete medicine records
* Display hash table buckets
* Compare search performance between hash table and array

### Question 2: Divide and Conquer Algorithm

Question 2 implements a system that sorts and searches customer transaction data using Merge Sort and Binary Search.

Main concepts covered:

* Divide and Conquer
* Merge Sort
* Binary Search
* Linear Search
* Recursion
* Performance Comparison

Main features:

* Transaction entity class
* Dataset of 20 unsorted transaction records
* Display transactions before sorting
* Sort transactions using Merge Sort
* Display transactions after sorting
* Show recursive Merge Sort calls
* Search existing and non-existing transactions using Binary Search
* Search transactions using Linear Search for comparison
* Insert transaction dynamically
* Sort by different attributes
* Count recursive calls
* Display time complexity analysis

### Question 3: Concurrent Process

Question 3 compares factorial calculation using multithreading and non-multithreading.

Main concepts covered:

* Factorial Calculation
* Big-O Time Complexity
* Multithreading
* Non-Multithreading
* Concurrent Processing
* Execution Time Measurement
* Performance Comparison

Main features:

* Factorial function for 50!, 100! and 200!
* Big-O derivation for the factorial function
* Three separate threads for factorial calculation
* Ten-round multithreading experiment
* Ten-round non-multithreading experiment
* Total and average time calculation in nanoseconds
* Final comparison between multithreaded and non-threaded execution

## Repository Structure

```text
Advanced-Algorithms-Assignment/
│
├── README.md
│
├── Question 1/
│   ├── Question_1.py
│   ├── README.md
│   ├── data/
│   │   └── sample_medicines.csv
│   └── src/
│       ├── __init__.py
│       ├── cli.py
│       ├── formatting.py
│       ├── hash_table.py
│       ├── inventory.py
│       ├── models.py
│       └── performance.py
│
├── Question 2/
│   ├── Question_2.py
│   ├── README.md
│   ├── data/
│   │   └── sample_transactions.csv
│   └── src/
│       ├── __init__.py
│       ├── cli.py
│       ├── formatting.py
│       ├── merge_sort.py
│       ├── models.py
│       ├── performance.py
│       ├── search.py
│       └── transaction_system.py
│
└── Question 3/
    ├── Question_3.py
    ├── README.md
    ├── sample_output.txt
    └── src/
        ├── __init__.py
        ├── analysis_text.py
        ├── cli.py
        ├── experiments.py
        ├── factorial.py
        ├── formatting.py
        └── models.py
```

## Folder Explanation

### `src` folder

The `src` folder contains the main source code modules. The code is separated into different files to improve readability, maintainability, and reusability.

Examples of source code modules include:

* entity classes
* algorithm implementation
* menu handling
* performance testing
* output formatting

### `data` folder

The `data` folder contains supporting sample datasets.

Examples:

* `sample_medicines.csv`
* `sample_transactions.csv`

## How to Run the Programs

Each question has its own main Python file.

### Run Question 1

```bash
cd Question_1_Hashing
python Question_1.py
```

### Run Question 2

```bash
cd Question_2_Divide_Conquer
python Question_2.py
```

### Run Question 3

```bash
cd Question_3_Concurrent_Process
python Question_3.py
```

The programs should be run from their own question folders so that the file paths for the `data` and `src` folders work correctly.

## Software Requirements

* Python 3.10 or later
* PyCharm, Visual Studio Code, or any Python-supported IDE
* No external Python libraries are required

## Python Concepts Used

This assignment applies the following Python concepts:

* Classes and objects
* Dataclasses
* Lists
* CSV file reading
* Recursion
* Functions
* Modular programming
* Command-line interface
* Time measurement
* Threading
* Error handling
* Formatted table output

## Algorithms and Data Structures Used

| Question   | Algorithm / Data Structure     | Purpose                              |
| ---------- | ------------------------------ | ------------------------------------ |
| Question 1 | Hash Table with Linear Probing | Fast medicine search                 |
| Question 1 | One-Dimensional Array Search   | Performance comparison               |
| Question 2 | Merge Sort                     | Sorting transaction records          |
| Question 2 | Binary Search                  | Searching sorted transaction records |
| Question 2 | Linear Search                  | Searching comparison                 |
| Question 3 | Factorial Algorithm            | CPU-bound calculation task           |
| Question 3 | Multithreading                 | Concurrent execution experiment      |


## Author

Student Name: Wong Khye Jean 
