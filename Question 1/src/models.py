"""
Entity models for the Pharmacy Inventory System.

This module contains data classes only. Keeping entity classes separate
makes them reusable in other programs and improves code readability.
"""

from dataclasses import dataclass


@dataclass
class Medicine:
    """
    Represents one pharmacy product.

    Attributes:
        medicine_id: Unique product ID used as the hash table key.
        name: Display name of the medicine.
        category: Product type such as Tablet, Syrup, Supplement, etc.
        dosage: Strength or volume, stored as text because it includes units.
        stock_quantity: Available stock count.
        price: Selling price.
    """

    medicine_id: str
    name: str
    category: str
    dosage: str
    stock_quantity: int
    price: float

    def to_row(self) -> list[str]:
        """
        Convert the medicine object into a list of formatted strings.
        Used by table display functions.
        """
        return [
            self.medicine_id,
            self.name,
            self.category,
            self.dosage,
            str(self.stock_quantity),
            f"RM {self.price:.2f}",
        ]

    def __str__(self) -> str:
        """Return a readable single-line description of the medicine."""
        return (
            f"{self.medicine_id} | {self.name} | {self.category} | "
            f"{self.dosage} | Stock Quantity: {self.stock_quantity} | RM {self.price:.2f}"
        )
