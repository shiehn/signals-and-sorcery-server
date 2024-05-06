from langchain_core.tools import BaseTool

from game_engine.api.storage import list_items, add_item


class ListItems(BaseTool):
    name = "ListItems"
    description = "List all of users items in their storage or inventory given a user_id. This tool takes one parameter user_id. It returns a list of items."

    def _run(self, user_id: str):
        return list_items(user_id)

    def _arun(self, *args, **kwargs):
        return self._run(*args, **kwargs)


class StoreItem(BaseTool):
    name = "StoreItem"
    description = "Add an item to the user's storage or inventory with the provided item_id.  This tool takes one parameter, item_id. It returns True if the item was successfully stored, otherwise False."

    def _run(self, item_id: str) -> bool:
        add_item(item_id)
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
