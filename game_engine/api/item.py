items = [
    {
        'item_id': 'necklace-x3e1',
        'size': '4x4in',
    },
    {
        'item_id': 'ring-r4r3',
        'size': '1x1in',
    },
    {
        'item_id': 'sword-z2z6',
        'size': '1x36in',
    },
    {
        'item_id': 'ball-555s',
        'size': '2x2in',
    },
]


def list_items():
    return items


def get_item(item_id):
    for item in items:
        if item['item_id'] == item_id:
            return item
    return None
