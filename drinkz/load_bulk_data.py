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
from . import recipes

def data_reader(fp):
    reader = csv.reader(fp)
    for line in reader:
        try:
            if line[0].startswith('#') or not line[0].strip():
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

    Loads in data of the form recipe name, amount: type, amount: type, ... from a CSV file.


    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.
    """
    new_reader = data_reader(fp)

    x = []
    n = 0

    while (1):
        try:
            for line in new_reader:
                try:
                    name = line[0]
                    tempInglist = line[1:]
                    ingList = []
                    for item in tempInglist:
                        amt,typ = item.split(":")
                        ingList.append((amt,typ))
                    newRecipe = recipes.Recipe(name, ingList)
                    n += 1
                    db.add_recipe(newRecipe)
                except ValueError:
                    print 'Your formatting is bad and you should feel bad: %s' % line
                    continue
            new_reader.next()
        except StopIteration:
            return n
    return n

