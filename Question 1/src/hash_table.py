"""
Reusable Hash Table implementation using Linear Probing.

This module is intentionally independent from the pharmacy system.
It can be reused for other key-value storage problems.
"""

from dataclasses import dataclass
from typing import Generic, Iterator, Optional, TypeVar


K = TypeVar("K")
V = TypeVar("V")


@dataclass
class HashEntry(Generic[K, V]):
    """
    Represents one occupied hash table bucket.

    Attributes:
        key: Search key stored in the bucket.
        value: Data object stored in the bucket.
    """

    key: K
    value: V


class DeletedEntry:
    """
    Marker object used for lazy deletion.

    In open addressing, deleted buckets cannot simply be changed to None
    because doing so may break a probing chain. A marker allows future
    searches to continue probing while still allowing the bucket to be reused.
    """


DELETED = DeletedEntry()


class LinearProbingHashTable(Generic[K, V]):
    """
    Hash Table using Open Addressing with Linear Probing.

    Bucket structure:
        self._buckets is a fixed-size Python list.
        Each bucket may contain:
            1. None       -> never used bucket
            2. DELETED    -> previously used bucket
            3. HashEntry  -> active key-value record

    Average time complexity:
        Search: O(1)
        Insert: O(1)
        Delete: O(1)

    Worst-case time complexity:
        O(n), usually caused by many collisions or a high load factor.
    """

    DEFAULT_MAX_LOAD_FACTOR = 0.70

    def __init__(
        self,
        capacity: int = 31,
        max_load_factor: float = DEFAULT_MAX_LOAD_FACTOR,
    ) -> None:
        if capacity <= 0:
            raise ValueError("Hash table capacity must be greater than 0.")

        if not 0 < max_load_factor < 1:
            raise ValueError("Maximum load factor must be between 0 and 1.")

        self._capacity = capacity
        self._max_load_factor = max_load_factor
        self._buckets: list[object] = [None] * capacity
        self._size = 0
        self._collision_count = 0

    @property
    def capacity(self) -> int:
        """Return the current number of buckets."""
        return self._capacity

    @property
    def size(self) -> int:
        """Return the number of active records stored."""
        return self._size

    @property
    def collision_count(self) -> int:
        """Return the number of collisions recorded during insertions."""
        return self._collision_count

    @property
    def load_factor(self) -> float:
        """Return how full the hash table currently is."""
        return self._size / self._capacity

    def _hash(self, key: K) -> int:
        """
        Stable string-based hash function.

        Python's built-in hash for strings may change between program runs.
        This custom polynomial hash gives consistent bucket positions, which
        makes screenshots and testing easier for an assignment.
        """
        key_text = str(key)
        hash_value = 0
        multiplier = 31

        for character in key_text:
            hash_value = (hash_value * multiplier + ord(character)) % self._capacity

        return hash_value

    def _probe_index(self, start_index: int, attempt: int) -> int:
        """
        Calculate the next bucket index using linear probing.

        Formula:
            next_index = (start_index + attempt) mod capacity
        """
        return (start_index + attempt) % self._capacity

    def _should_resize(self) -> bool:
        """Check whether the table should be resized before insertion."""
        return self.load_factor >= self._max_load_factor

    def _resize(self) -> None:
        """
        Resize the hash table and reinsert existing records.

        This improves performance by reducing clustering when the table
        becomes too full.
        """
        old_entries = list(self.items())

        self._capacity = self._capacity * 2 + 1
        self._buckets = [None] * self._capacity
        self._size = 0
        self._collision_count = 0

        for key, value in old_entries:
            self.insert(key, value)

    def insert(self, key: K, value: V) -> None:
        """
        Insert or update a key-value record.

        If the key already exists, its value is replaced.
        """
        if self._should_resize():
            self._resize()

        start_index = self._hash(key)
        first_deleted_index: Optional[int] = None

        for attempt in range(self._capacity):
            current_index = self._probe_index(start_index, attempt)
            bucket = self._buckets[current_index]

            if bucket is DELETED:
                if first_deleted_index is None:
                    first_deleted_index = current_index
                continue

            if bucket is None:
                target_index = (
                    first_deleted_index
                    if first_deleted_index is not None
                    else current_index
                )
                self._buckets[target_index] = HashEntry(key, value)
                self._size += 1
                return

            if isinstance(bucket, HashEntry) and bucket.key == key:
                bucket.value = value
                return

            self._collision_count += 1

        raise RuntimeError("Hash table insertion failed because no bucket was found.")

    def search(self, key: K) -> Optional[V]:
        """
        Search for a value by key.

        Returns:
            The stored value if found, otherwise None.
        """
        start_index = self._hash(key)

        for attempt in range(self._capacity):
            current_index = self._probe_index(start_index, attempt)
            bucket = self._buckets[current_index]

            if bucket is None:
                return None

            if bucket is DELETED:
                continue

            if isinstance(bucket, HashEntry) and bucket.key == key:
                return bucket.value

        return None

    def delete(self, key: K) -> bool:
        """
        Delete a record by key using lazy deletion.

        Returns:
            True if deleted, False if the key was not found.
        """
        start_index = self._hash(key)

        for attempt in range(self._capacity):
            current_index = self._probe_index(start_index, attempt)
            bucket = self._buckets[current_index]

            if bucket is None:
                return False

            if bucket is DELETED:
                continue

            if isinstance(bucket, HashEntry) and bucket.key == key:
                self._buckets[current_index] = DELETED
                self._size -= 1
                return True

        return False

    def items(self) -> Iterator[tuple[K, V]]:
        """Yield active key-value pairs from the hash table."""
        for bucket in self._buckets:
            if isinstance(bucket, HashEntry):
                yield bucket.key, bucket.value

    def bucket_rows(self) -> list[list[str]]:
        """
        Return formatted bucket information for display.

        This is useful for showing how linear probing stores data.
        """
        rows: list[list[str]] = []

        for index, bucket in enumerate(self._buckets):
            if bucket is None:
                rows.append([str(index), "EMPTY", "-", "-"])
            elif bucket is DELETED:
                rows.append([str(index), "DELETED", "-", "-"])
            elif isinstance(bucket, HashEntry):
                rows.append([str(index), "OCCUPIED", str(bucket.key), str(bucket.value)])

        return rows
