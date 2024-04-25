storage = []


def add_item(item):
    storage.append(item)

def remove_item(item_id):
    for i, item in enumerate(storage):
        if item['item_id'] == item_id:
            storage.pop(i)
            return True
    return False

def list_items():
    return storage
