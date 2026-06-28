"""
Pharmacy inventory logic.

This module separates business logic from the command-line interface.
"""

import csv
from datetime import date
from pathlib import Path
from typing import Optional

from src.hash_table import LinearProbingHashTable
from src.models import Medicine


class PharmacyInventory:
    """
    Manages pharmacy medicine records.

    The inventory stores the same medicine data in:
        1. Hash table       -> fast search by medicine ID
        2. One-dimensional array -> used for performance comparison
    """

    def __init__(self, table_capacity: int = 31) -> None:
        self._hash_table: LinearProbingHashTable[str, Medicine] = (
            LinearProbingHashTable(capacity=table_capacity)
        )
        self._medicine_array: list[Medicine] = []

    @property
    def hash_table(self) -> LinearProbingHashTable[str, Medicine]:
        """Return the internal hash table."""
        return self._hash_table

    @property
    def medicine_array(self) -> list[Medicine]:
        """Return the one-dimensional array of medicine records."""
        return self._medicine_array

    def load_from_csv(self, file_path: Path) -> int:
        """
        Load sample medicines from a CSV file.

        Args:
            file_path: Path to CSV data file.

        Returns:
            Number of records loaded.
        """
        loaded_count = 0

        with file_path.open("r", encoding="utf-8", newline="") as csv_file:
            reader = csv.DictReader(csv_file)

            for row in reader:
                medicine = Medicine(
                    medicine_id=row["medicine_id"].strip().upper(),
                    name=row["name"].strip(),
                    category=row["category"].strip(),
                    dosage=row["dosage"].strip(),
                    stock_quantity=int(row["stock_quantity"]),
                    price=float(row["price"]),
                    expiry_date=date.fromisoformat(row["expiry_date"]),
                )
                self.insert_medicine(medicine)
                loaded_count += 1

        return loaded_count

    def insert_medicine(self, medicine: Medicine) -> None:
        """
        Insert or update a medicine in both data structures.
        """
        medicine.medicine_id = medicine.medicine_id.strip().upper()

        existing_medicine = self.search_by_hash_table(medicine.medicine_id)
        self._hash_table.insert(medicine.medicine_id, medicine)

        if existing_medicine is None:
            self._medicine_array.append(medicine)
            return

        for index, item in enumerate(self._medicine_array):
            if item.medicine_id == medicine.medicine_id:
                self._medicine_array[index] = medicine
                return

    def search_by_hash_table(self, medicine_id: str) -> Optional[Medicine]:
        """
        Search for a medicine using the hash table.
        """
        return self._hash_table.search(medicine_id.strip().upper())

    def search_by_array(self, medicine_id: str) -> Optional[Medicine]:
        """
        Search for a medicine using sequential search in a one-dimensional array.
        """
        target_id = medicine_id.strip().upper()

        for medicine in self._medicine_array:
            if medicine.medicine_id == target_id:
                return medicine

        return None

    def update_medicine(
        self,
        medicine_id: str,
        stock_quantity: Optional[int] = None,
        price: Optional[float] = None,
    ) -> bool:
        """
        Update medicine stock_stock quantity and/or price.

        Returns:
            True if update is successful, otherwise False.
        """
        medicine = self.search_by_hash_table(medicine_id)

        if medicine is None:
            return False

        if stock_quantity is not None:
            medicine.stock_quantity = stock_quantity

        if price is not None:
            medicine.price = price

        return True

    def delete_medicine(self, medicine_id: str) -> bool:
        """
        Delete medicine from both the hash table and the array.

        Returns:
            True if deletion is successful, otherwise False.
        """
        target_id = medicine_id.strip().upper()
        deleted = self._hash_table.delete(target_id)

        if deleted:
            self._medicine_array = [
                medicine
                for medicine in self._medicine_array
                if medicine.medicine_id != target_id
            ]

        return deleted

    def get_inventory_rows(self) -> list[list[str]]:
        """
        Return all medicine records as formatted table rows.
        """
        return [medicine.to_row() for medicine in self._medicine_array]

    def get_bucket_rows(self) -> list[list[str]]:
        """
        Return hash table bucket rows for display.
        """
        return self._hash_table.bucket_rows()

    def get_statistics_rows(self) -> list[list[str]]:
        """
        Return hash table statistics as rows for formatted display.
        """
        return [
            ["Total active records", str(self._hash_table.size)],
            ["Hash table capacity", str(self._hash_table.capacity)],
            ["Load factor", f"{self._hash_table.load_factor:.2f}"],
            ["Collision count during insertions", str(self._hash_table.collision_count)],
        ]
