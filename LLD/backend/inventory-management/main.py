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



