from typing import TypeVar, Optional, Generic
from sortedcontainers import SortedList

T = TypeVar("T")

class PriorityQueue(Generic[T]):

    def __init__(self):
        self.queue: SortedList[T] = SortedList(key = self.get_priority)
        self.priorities: dict[T, float] = dict()
    
    def get_priority(self, element: T) -> float:
        return self.priorities[element]

    def insert(self, element: T, priority: float):
        self.priorities[element] = priority
        self.queue.add(element)

    def get_minimum(self) -> Optional[T]:
        return self.queue[0] if self.queue else None

    def extract_minimum(self) -> Optional[T]:
        element = None
        if self.queue:
            element = self.queue.pop(0)
            self.priorities.pop(element)
        return element

    def remove(self, element: T):
        self.queue.remove(element)
        self.priorities.pop(element)
    
    def discard(self, element: T):
        if element in self:
            self.queue.remove(element)
    
    def __iter__(self):
        return iter(self.queue)

    def __repr__(self) -> str:
        return ', '.join([str(e) for e in self])

    def __contains__(self, element: T) -> bool:
        return element in self.priorities

if __name__ == '__main__':
    # Example Usage
    pq = PriorityQueue()
    a, b, c, d = "A", "B", "C", "asda"
    pq.insert(a, 0)
    pq.insert(b, 1)
    pq.insert(c, -1)
    pq.insert(d, 0.2)

    print(pq)
    print(pq.get_minimum())

    pq.remove(a)
    print(pq)
    pq.remove("C")
    print(pq)