"""
Lab 7: The Collision Resolver -- starter.

Complete the three classes below. See
Lab_07_The_Collision_Resolver.md, Part B, for the full requirements.
"""

from typing import Generic, Hashable, List, Optional, Tuple, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")

_TOMBSTONE = object()  # sentinel marking a deleted open-addressing slot


class _ChainNode(Generic[K, V]):
    __slots__ = ("key", "value", "next")

    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value
        self.next: Optional["_ChainNode[K, V]"] = None


class ChainedHashMap(Generic[K, V]):
    """Separate chaining: each bucket is a linked list of (key, value)."""

    def __init__(self, initial_size: int = 16) -> None:
        self._buckets: List[Optional[_ChainNode[K, V]]] = [None] * initial_size
        self._count = 0

    def __len__(self) -> int:
        return self._count

    def insert(self, key: K, value: V) -> None:
        """Insert, or update in place if `key` already exists. Resize (double + rehash) once load factor > 0.75."""
        index = hash(key) % len(self._buckets)
        node = self._buckets[index]

        # update the node's value
        while node is not None:
            if node.key == key:
                node.value = value
                return
            node = node.next

        # insert if it hits None
        new_node = _ChainNode(key, value)
        new_node.next = self._buckets[index] 
        self._buckets[index] = new_node
        self._count += 1

        # resize check
        if self._count / len(self._buckets) > 0.75:
            self.resize()

    # resizing method
    def resize(self) -> None:
        old_buckets = self._buckets
        self._buckets = [None] * (len(old_buckets) * 2)
        self._count = 0
        for bucket in old_buckets:
            node = bucket
            while node is not None:
                self.insert(node.key, node.value)
                node = node.next




    def get(self, key: K) -> V:
        """Return the value for `key`. Raise KeyError if missing."""
        index = hash(key) % len(self._buckets)
        node = self._buckets[index]
        while node is not None:
            if node.key == key:
                return node.value
            node = node.next
        raise KeyError(f"There is no node with key: {key}")

    def delete(self, key: K) -> None:
        """Remove `key`. Raise KeyError if missing."""
        index = hash(key) % len(self._buckets)
        node = self._buckets[index]
        prev_node = None
        while node is not None:
            if node.key == key:
                if prev_node is None:
                    self._buckets[index] = node.next
                else:
                    prev_node.next = node.next
                self.count -= 1
                return
            prev_node = node
            node = node.next   
        raise KeyError(f"There is no node with key: {key}")


class LinearProbingHashMap(Generic[K, V]):
    """Open addressing with linear probing and tombstone deletion."""

    def __init__(self, initial_size: int = 16) -> None:
        self._keys: List[object] = [None] * initial_size
        self._values: List[Optional[V]] = [None] * initial_size
        self._count = 0

    def __len__(self) -> int:
        return self._count

    def insert(self, key: K, value: V) -> None:
        """Resize (double + rehash) once load factor > 0.7."""

        # resize check
        if (self._count) / len(self._keys) > 0.7:
            self.resize()


        index = hash(key) % len(self._keys)
        first_tombstone = None

        for i in range(len(self._keys)):

            slot = (index + i) % len(self._keys)

            # inserts immediately if it hits None or at first_tombstone if we hit a tombstone while probing
            if self._keys[slot] is None:
                if first_tombstone is None:
                    self._keys[slot] = key
                    self._values[slot] = value
                else:
                    self._keys[first_tombstone] = key
                    self._values[first_tombstone] = value
                self._count += 1
                return

            # records the spot of TOMBSTONE and checks to see if any of the next keys are matching to prevent duplicate keys
            elif self._keys[slot] is _TOMBSTONE:
                if first_tombstone is None:
                    first_tombstone = slot

            # updates if it finds a mathcing key
            elif self._keys[slot] == key:
                self._values[slot] = value
                return

        # insert at first tombstone since it never hit None after a full loop through
        self._keys[first_tombstone] = key
        self._values[first_tombstone] = value
        self._count += 1
        return
            

    def resize(self) -> None:
        old_keys = self._keys
        old_values = self._values
        self._keys = [None] * (len(old_keys) * 2)
        self._values = [None] * (len(old_values) * 2)
        self._count = 0
        for i in range(len(old_keys)):
            if old_keys[i] is not None and old_keys[i] is not _TOMBSTONE:
                self.insert(old_keys[i], old_values[i])

    def search(self, key: K) -> V:
        """Return the value for `key`. Raise KeyError if missing."""
        index = hash(key) % len(self._keys)
        for i in range(len(self._keys)):
            slot = (index + i) % len(self._keys)
            if self._keys[slot] is None:
                break
            if self._keys[slot] is _TOMBSTONE:
                continue 
            if self._keys[slot] == key:
                return self._values[slot]
        raise KeyError(f"There is no value for the key: {key} in the list")

    def delete(self, key: K) -> None:
        """Remove `key` using a tombstone (not None) so later probes don't stop early. Raise KeyError if missing."""
        index = hash(key) % len(self._keys)
        for i in range(len(self._keys)):
            slot = (index + i) % len(self._keys)
            if self._keys[slot] is None:
                break
            elif self._keys[slot] is _TOMBSTONE:
                continue
            elif self._keys[slot] == key:
                self._keys[slot] = _TOMBSTONE
                self._values[slot] = None
                self._count -= 1
                return
        raise KeyError(f"There is no key: {key} to delete in the list")
            
            


class QuadraticProbingHashMap(Generic[K, V]):
    """
    Open addressing with quadratic probing and tombstone deletion.

    Pitfall to design around: with a power-of-2 table size, the probe
    sequence (idx + i^2) mod size does NOT reach every slot -- it can
    cycle through only about half of them, so the table can appear
    "full" and raise/loop forever even though empty slots exist
    elsewhere. Two standard fixes, pick one:
      (a) use a PRIME table size (so the quadratic sequence covers all
          slots whenever load factor < 1), or
      (b) resize proactively -- check load factor BEFORE attempting an
          insert's probe sequence, not only after a successful insert.
    Using both is safest.
    """

    def __init__(self, initial_size: int = 17) -> None:
        self._keys: List[object] = [None] * initial_size
        self._values: List[Optional[V]] = [None] * initial_size
        self._count = 0

    def __len__(self) -> int:
        return self._count

    def insert(self, key: K, value: V) -> None:
        """Resize (grow + rehash) once load factor > 0.7 -- see the pitfall note above."""
        # TODO
        raise NotImplementedError

    def search(self, key: K) -> V:
        """Return the value for `key`. Raise KeyError if missing."""
        # TODO
        raise NotImplementedError

    def delete(self, key: K) -> None:
        """Remove `key` using a tombstone. Raise KeyError if missing."""
        # TODO
        raise NotImplementedError
