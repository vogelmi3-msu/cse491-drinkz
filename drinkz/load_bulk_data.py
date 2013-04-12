"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package

from . import db                        # import from local package
import recipes

def data_reader(fp):
    reader = csv.reader(fp)
    for line in reader:
        try:
            if line[0].startswith('#'):
                continue
            if not line[0].strip():
                continue
        except IndexError:
            continue
        yield line
        

def load_bottle_types(fp):
    """
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """
    new_reader = data_reader(fp)
    x = []
    n = 0
    while (1):
        try:
            for line in new_reader:
                try:
                    (mfg, name, typ)= line
                    n += 1
                    db.add_bottle_type(mfg, name, typ)
                except ValueError:
                    continue

            new_reader.next()
        except StopIteration:
            return n
    return n



def load_inventory(fp):
    """
    Loads in data of the form manufacturer/liquor name/amount from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """
    new_reader = data_reader(fp)

    x = []
    n = 0

    while (1):
        try:
            for line in new_reader:
                try:
                    (mfg, liquor, amount)= line
                    n += 1
                    db.add_to_inventory(mfg, liquor, amount)
                except ValueError:
                    continue
            new_reader.next()
        except StopIteration:
            return n
    return n

def load_recipes(fp):
    """
    Loads in data of the form manufacturer/liquor name/amount from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """
    new_reader = data_reader(fp)

    x = []
    n = 0

    while (1):
        try:
            for line in new_reader:
                try:
                    splitLine = line.split(',')
                    name = splitLine[0]
                    ingredients = splitLine[1:]
                    ingredient_list = []
                    for item in ingredients:
                        (amt,typ) = item.split(':')
                        ingredient_list.append((amt,typ))
                    r=Recipe(name,ingredient_list)
                    
                    n += 1
                    db.add_recipe(r)
                except ValueError:
                    continue
            new_reader.next()
        except StopIteration:
            return n
    return n

