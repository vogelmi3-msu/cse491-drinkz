"""
Database functionality for drinkz information.
"""

from cPickle import dump, load
import recipes as rc
import sys
import os.path
import sqlite

try:
    os.unlink('tables.db')
except OSError:
    pass

db = sqlite3.connect('tables.db')
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

c = db.cursor()

def _create_db(filename):
    # private singleton variables at module level
    global c
    c.execute('CREATE TABLE _bottle_types_db (id INTEGER PRIMARY KEY ASC, manufacturer TEXT, type TEXT, liquor TEXT)')
    c.execute('CREATE TABLE _inventory_db (id INTEGER PRIMARY KEY ASC, name TEXT, liquor TEXT, amount FLOAT, bottle_type_id INTEGER)')
    c.execute('CREATE TABLE _recipe_db (id INTEGER PRIMARY KEY ASC, name TEXT, ingredient_list TEXT)')
    temp_bottle_types_db =set()
    temp_inventory_db ={}
    temp_recipe_db = {}
    fp = open(filename,'rb')
    loaded = load(fp)
    (temp_bottle_types_db,temp_inventory_db,temp_recipe_db)=loaded
    print loaded

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global c
    c.execute('DELETE FROM _bottle_types_db WHERE 1')
    c.execute('DELETE FROM _inventory_db WHERE 1')
    c.execute('DELETE FROM _recipe_db WHERE 1')

def load_db():

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

class YourRecipeFormatSucks(Exception):
    pass

def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    global c
    c.execute('IF NOT EXISTS( SELECT 1 FROM _bottle_types_db WHERE manufacturer=",mfg,", AND liquor=",liquor,"" AND type=",typ,"") INSERT INTO _bottle_types_db (manufacturer, liquor, type) VALUES("mfg,",",liquor,",",typ,"")')

def _check_bottle_type_exists(mfg, liquor):
    global c
    c.execute('SELECT id FROM _bottle_types_db WHERE manufacturer=',mfg,' AND liquor=',liquor)
    bottle_type_id =  c.fetchone()[0]
    if bottle_type_id > 0:
            return True 
    return False

def _check_recipe_exists(name):
    global c
    c.execute('SELECT id FROM _bottle_types_db WHERE name=',name)
    recipe_id =  c.fetchone()[0]
    if recipe_id > 0:
            return True 
    return False

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    global c
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)    
        pass

    # check for key in dict, if  present, append list
    try:
        amt = convert_to_ml(amount)
    except (ValueError):
        err = "Invalid input: missing amount"
        raise InvalidInput(err)
    oldAmount = c.execute('SELECT amount FROM _inventory_db WHERE manufacturer=',mfg,' AND liquor=',liquor)
    if oldAmount > 0:
        c.execute('(UPDATE _inventory_db SET amount=",amount+oldAmount")')
    else:
        bottle_type_id = c.execute("(SELECT id FROM _bottle_types_db WHERE manufacturer=',mfg,' AND liquor=',liquor)")
        c.execute("(INSERT INTO _inventory_db (manufacturer, liquor, amount, id) VALUES('mfg,',',liquor,',',typ,',',bottle_type_id,')")
        

def check_inventory(mfg, liquor):
    global c
    c.execute("(SELECT id FROM _inventory_db WHERE manufacturer=',mfg,'AND liquor=',liquor)")
    liquor_id =  c.fetchone()[0]
    if liquor_id > 0:
            return True 
    return False

def check_inventory_for_type(typ):
    global c
    c.execute('SELECT id FROM _inventory_db WHERE type=',typ)
    liquor_id =  c.fetchone()[0]
    if liquor_id > 0:
            return True 
    return False


def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    global c
    _inventory_db = c.execute("(SELECT amount FROM _inventory_db WHERE manufacturer=',mfg,' AND liquor=',liquor)")
    amount = c.fetchone()[0] 
    return amount

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
    global c
    _inventory_db = c.execute('SELECT * FROM _inventory_db')
    for i in _inventory_db:
        yield i['manufacturer'], i['liquor']

def add_recipe(r):
    global c
    ingredients = ','.join(r.ingredient_list)
    c.execute("(IF NOT EXISTS( SELECT 1 FROM _recipe_db WHERE name=',r.getName(),') INSERT INTO _recipe_db (name, ingredient_list) VALUES('r.getName(),',',ingredients')")
    key = r.getName()
    value = r
    if (get_recipe(key)):
        err = "recipe name in Database"
        raise DuplicateRecipeName(err)
    else:
        _recipe_db[key] = value

def get_recipe(name):
    global c
    c.execute("(SELECT ingredient_list FROM _recipe_db WHERE name=',name)")
    ingredients =  c.fetchone()[0]
    if ingredients:
        return Recipe(name,ingredients.split(','))
    return False

def get_all_recipes():
    global c
    c.execute('SELECT * FROM _recipe_db')
    return c.fetchall()

def get_inventory():
    global c
    c.execute('SELECT * FROM _inventory_db')
    return  c.fetchall()

def recipes_we_can_make():
    recipes_we_can_make_list = []
    _recipe_db = get_all_recipes()
    for recipe in _recipe_db:
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
            recipes_we_can_make_list.append(recipe)
    return recipes_we_can_make_list

