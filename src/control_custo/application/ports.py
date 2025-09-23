from abc import ABC, abstractmethod
from typing import List
from ..domain.models import Item

class ItemRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Item]:
        pass

    @abstractmethod
    def get_by_id(self, item_id: int) -> Item | None:
        pass

    @abstractmethod
    def create(self, item: Item) -> Item:
        pass
