"""
Database functionality for drinkz information.
"""

from cPickle import dump, load
import recipes as rc

# private singleton variables at module level
_bottle_types_db =set()
_inventory_db ={}
_recipe_db = {}

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipe_db
    _bottle_types_db =set()
    _inventory_db = {}
    _recipe_db = {}

def save_db(filename):
    fp = open(filename, 'wb')

    tosave = (_bottle_types_db, _inventory_db, _recipe_db)
    dump(tosave, fp)

    fp.close()

def load_db(filename):
    global _bottle_types_db, _inventory_db, _recipe_db
    fp = open(filename, 'rb')

    loaded = load(fp)
    (_bottle_types_db, _inventory_db, _recipe_db) = loaded

    fp.close()

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass

class InvalidInput(Exception):
    pass

class DuplicateRecipeName(Exception):
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

def check_inventory_for_type(typ):
    available = []
    for (m, l, t) in _bottle_types_db:
        if t == typ:
            available.append((m,l))
    return available



def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    amounts = _inventory_db[(mfg, liquor)] 
    totalVolume = 0.0
    for bottle in amounts:
        totalVolume += convert_to_ml(bottle)
    return totalVolume

def convert_to_ml(amount):
    (amt, unit) = amount.split()
    if unit == "oz":
        volume = float(amt) * 29.5735
    elif unit == "gallon" or unit == "Gallon":
        volume =float(amt) * 3785.41
    elif unit == "liter" or unit == "Liter":
        volume = float(amt) * 1000.00
    else:
        volume = float(amt)
    return volume


def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for key in _inventory_db:
        yield key[0], key[1]

def add_recipe(r):
    key = r.getName()
    value = r
    if (get_recipe(key)):
        err = "recipe name in Database"
        raise DuplicateRecipeName(err)
    else:
        _recipe_db[key] = value

def get_recipe(name):
    try:
        return _recipe_db[name]
    except(KeyError):
        pass

def get_all_recipes():
    return _recipe_db.values()

def get_inventory():
    return _inventory_db

def recipes_we_can_make():
    recipes_we_can_make_list = []
    for name in _recipe_db:
        recipe = _recipe_db[name]
        print recipe
        ingredient_list = recipe.getIngredients()
        all_ingred = []
        for (typ,amt) in ingredient_list:
            
            avail = check_inventory_for_type(typ)
            avail_amt = 0
            for (m,l) in avail:
                avail_amt += get_liquor_amount(m,l)
            
            if avail_amt > convert_to_ml(amt):
                all_ingred.append(avail_amt)
        if len(all_ingred) == len(ingredient_list):
            print "hells yes"
            recipes_we_can_make_list.append(recipe)

    print recipes_we_can_make_list
    return recipes_we_can_make_list

