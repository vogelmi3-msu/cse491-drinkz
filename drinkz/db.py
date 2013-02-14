"""
Database functionality for drinkz information.
"""

# private singleton variables at module level
_bottle_types_db =set()
_inventory_db =[]

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db
    _bottle_types_db =set()
    _inventory_db = {}

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass

class InvalidInput(Exception):
    pass

def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True
    return False

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)
    
        pass

    # check for key in dict, if  present, append list
    try:
        amt = amount.split()
    except (ValueError):
        err = "Invalid input: missing amount"
        raise InvalidInput(err)
    
    try:
        _inventory_db[(mfg,liquor)].append(amount)

    # if not present, add to dict and create list
    except (KeyError):
        _inventory_db[(mfg,liquor)]=[amount]
        

def check_inventory(mfg, liquor):
    for key in _inventory_db:
        if mfg == key[0] and liquor == key[1]:
            return True
        
    return False

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    amounts = _inventory_db[(mfg, liquor)]
    totalVolume = 0.0

    for bottle in amounts:
        amt = bottle.split()
        if amt[1] == "oz":
            totalVolume += float(amt[0]) * 29.5735
        else:
            totalVolume += float(amt[0])
            
    return totalVolume

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for key in _inventory_db:
        yield key[0], key[1]
