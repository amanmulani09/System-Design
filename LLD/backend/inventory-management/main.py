"""
## Funtional requirements
1. add new items to inventory (name qty, price)
2. update quantity 
3. fetch item details by id 
4. remove item from inventory 
5. list all current items

## Non functional requirements
1. in-memory storage.
2. thread safe operation.
3. Easy to extend. (open/close principle)

## algorithm & design pattern choice.

1. inventory lookup needs O(1) operations. 
    Hashmap/dict 
2. ID Generation : simple incremental counter

"""

import threading

class Item:
    def __init__(self,item_id,name,quantity,price):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity
        self.price = price

    def __repr__(self):
        return f"Item(id={self.item_id}, name={self.name}, quantity={self.quantity}, price={self.price})"

class Inventory:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.items = {}
        self.item_id = 0
        self.lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = cls()
        return cls._instance    