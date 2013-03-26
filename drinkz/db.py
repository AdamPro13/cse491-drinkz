"""
Database functionality for drinkz information.

Recipes are stored in dictionaries, because it is far easier to 
access a recipe by name. In a set, it would be a tad rough, methinks.

A list is a laughable idea. 
"""

# private singleton variables at module level
_inventory_db = {}
_bottle_types_db = set()
_recipes_db = {}

from recipes import Recipe



def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipes_db
    _bottle_types_db = set()
    _inventory_db = {}
    _recipes_db = {}

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
    pass
    
class DuplicateRecipeName(Exception):
    pass


def add_recipe(r):
    "add a recipe to the database"
    
    if r.name in _recipes_db.keys():
        err = "Repeated recipe"
        raise DuplicateRecipeName(err)
    _recipes_db[r.name] = r
    
def get_all_recipes():
    "return all dem recipes"
    return _recipes_db.values()
    
def get_recipe(name):
    "gets a recipe (if it exists)"
    
    if name in _recipes_db:
        return _recipes_db[name]
    else:
        return False
    
def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False

def check_inventory_for_type(typ):
    "checks for a generic type and returns a list of mfg/liquor touples"
    
    available = []
    
    for (m, l, t) in _bottle_types_db:
        if t == typ:
            available.append((m,l))
    
    return available
            

def add_to_inventory(mfg, liquor, amount):
    "Add the given liquor/amount to inventory."
    if not _check_bottle_type_exists(mfg, liquor):
        err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
        raise LiquorMissing(err)
    
    addThis = (mfg, liquor)

    # just add it to the inventory database as a tuple, for now.
    if addThis in _inventory_db:
        _inventory_db[addThis].append(amount)
    else:
        _inventory_db[addThis] = []
        _inventory_db[addThis].append(amount)

def check_inventory(mfg, liquor):
    for (m, l) in _inventory_db.keys():
        if mfg == m and liquor == l:
            return True
        
    return False
    
def convert_to_ml(amount):
    "takes in a string amount and returns a float"
    
    #conversion rates
    #more could be added...
    ozToMl =  29.5735296
    galToML = 3785.41
    literToML = 1000.0
    
    amount = amount.strip()
    amount = amount.split(' ')
    unit = amount[1]
    amount = amount[0]
    
    if 'ml' in unit:
        amount = float(amount)
    elif 'oz' in unit:
        amount = float(amount) * ozToMl
    elif 'gallon' in unit:
        amount = float(amount) * galToML
    elif 'liter' in unit:
        amount = float(amount) * literToML

    
    
    return amount


def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."

    amounts = _inventory_db[(mfg, liquor)]

    total = 0
    
    for amount in amounts:
        amount = convert_to_ml(amount)  
        total += amount
        

    return total

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for (m, l) in _inventory_db.keys():
        yield m, l
