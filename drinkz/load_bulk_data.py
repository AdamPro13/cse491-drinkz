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

def data_reader(fp):
    """
    Generic Generator (I call him Jerry) for loading bulk data into our
    drinkz database.
    
    Takes a file pointer
    
    iterates through csv file
    
    yields 3 item touple of data to be used by the calling function
    """
    
    reader = csv.reader(fp)
    
    for line in reader:
        if not ''.join(line).strip():
            continue
        elif line[0].startswith('#'):
            continue
            
        (item1, item2, item3) = line
        
        item1 = item1.strip()
        item2 = item2.strip()
        item3 = item3.strip()
            
        yield (item1, item2, item3)
        

def load_bottle_types(fp):
    """
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """
    
    reader = data_reader(fp)
    n = 0
    for mfg, name, typ in reader:
        try:
            db.add_bottle_type(mfg, name, typ)
            n+=1
        except db.LiquorMissing:
            print "Could not add", mfg, name, typ
            continue
            

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

    reader = data_reader(fp)  
    n = 0
    for mfg, name, amount in reader:
        
        try:
            db.add_to_inventory(mfg, name, amount)
            n+=1
        except db.LiquorMissing:
            print "Could not add", mfg, name, amount
            continue

    return n
