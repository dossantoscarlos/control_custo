from typing import List
from .ports import ItemRepository
from ..domain.models import Item

class ItemService:
    def __init__(self, repository: ItemRepository):
        self.repository = repository

    def get_all_items(self) -> List[Item]:
        return self.repository.get_all()

    def create_item(self, name: str, description: str) -> Item:
        # In a real application, you would have more business logic here
        new_item = Item(id=self.repository.get_next_id(), name=name, description=description)
        return self.repository.create(new_item)
