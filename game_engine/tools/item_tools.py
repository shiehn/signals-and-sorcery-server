from langchain_core.tools import BaseTool

from game_engine.api.item import get_item
from game_engine.api.storage import list_items, add_item


class ListItems(BaseTool):
    name = "ListItems"
    description = (
        "List all of users items in storage.  This tool does take any parameters."
    )

    def _run(self, *args, **kwargs):
        return list_items()

    def _arun(self, *args, **kwargs):
        return self._run(*args, **kwargs)


class StoreItem(BaseTool):
    name = "StoreItem"
    description = "Add an item to the user's storage with the provided item_id.  This tool takes one parameter, item_id. It returns True if the item was successfully stored, otherwise False."

    def _run(self, item_id: str) -> bool:
        item = get_item(item_id)
        if not item:
            return False

        add_item(item)
        return True

    def _arun(self, item_id: str) -> bool:
        return self._run(item_id)


class RemoveItem(BaseTool):
    name = "RemoveItem"
    description = "Remove an item from the user's storage with the provided item_id.  This tool takes one parameter, item_id. It returns True if the item was successfully removed, otherwise False."

    def _run(self, item_id: str) -> bool:
        return self._remove(item_id)

    def _arun(self, item_id: str) -> bool:
        return self._run(item_id)
