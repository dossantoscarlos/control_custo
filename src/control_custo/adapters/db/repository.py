from typing import List
from ...application.ports import ItemRepository
from ...domain.models import Item

class InMemoryItemRepository(ItemRepository):
    _items: List[Item] = []

    def get_all(self) -> List[Item]:
        return self._items

    def get_by_id(self, item_id: int) -> Item | None:
        for item in self._items:
            if item.id == item_id:
                return item
        return None

    def create(self, item: Item) -> Item:
        self._items.append(item)
        return item

    def get_next_id(self) -> int:
        return len(self._items) + 1
