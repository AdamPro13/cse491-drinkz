"""
Database functionality for drinkz information.
"""

# private singleton variables at module level
_inventory_db = {}
_bottle_types_db = set()



def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db
    _bottle_types_db = set()
    _inventory_db = {}

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class LiquorMissing(Exception):
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

def get_liquor_amount(mfg, liquor):
    "Retrieve the total amount of any given liquor currently in inventory."
    
    #conversion rate: ml to Fl Oz
    ozToMl =  29.5735296
    galToML = 3785.41
    
    amounts = _inventory_db[(mfg, liquor)]

    total = 0
    
    for amount in amounts:
        print amount
        if 'ml' in amount:
            #get rid of extra spaces
            amount = amount.strip()
            amount = amount.strip('ml')
            amount = float(amount)
        elif 'oz' in amount:
            amount = amount.strip()
            amount = amount.strip('oz')
            amount = float(amount)
            amount = amount * ozToMl
        elif 'gallon' in amount:
            amount = amount.strip()
            amount = amount.split(' ')
            amount = amount[0]
            amount = float(amount) * galToML

            
        total += amount
        

    return total

def get_liquor_inventory():
    "Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for (m, l) in _inventory_db.keys():
        yield m, l
