"""
Test code to be run with 'nosetests'.

Any function starting with 'test_', or any class starting with 'Test', will
be automatically discovered and executed (although there are many more
rules ;).
"""

import sys
sys.path.insert(0, 'bin/') # allow _mypath to be loaded; @CTB hack hack hack

from cStringIO import StringIO
import imp

from . import db, load_bulk_data

def test_foo():
    # this test always passes; it's just to show you how it's done!
    print 'Note that output from passing tests is hidden'

def test_add_bottle_type_1():
    print 'Note that output from failing tests is printed out!'
                
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')

def test_add_to_inventory_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

def test_add_to_inventory_2():
    db._reset_db()

    try:
        db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
        assert False, 'the above command should have failed!'
    except db.LiquorMissing:
        # this is the correct result: catch exception.
        pass

def test_get_liquor_amount_1():
    ''' make sure amounts add '''
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '5000 ml')
    
    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 6000.0, amount
    
def test_get_liquor_amount_2():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')

    data = "Johnnie Walker,Black Label,1000 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1000.0, amount

def test_get_liquor_amount_3():
    '''Test amount conversion with oz'''
    db._reset_db()
    
    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', ' 50 oz ')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '5000 ml')
    
    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount ==  6478.67648, amount


def test_bulk_load_inventory_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1000 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    assert db.check_inventory('Johnnie Walker', 'Black Label')
    assert n == 1, n
    
def test_bulk_load_inventory_2():
    ''' make sure inventory skips over commented lines'''
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')

    data = "#Johnnie Walker,Black Label,1000 ml\n#hello"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    assert not db.check_inventory('Johnnie Walker', 'Black Label')
    assert n == 0, n

def test_bulk_load_inventory_3():
    ''' make sure inventory skips over empty lines'''
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_bottle_type('Old Ezra', 'whiskey', 'whiskey')

    data = "\nJohnnie Walker,Black Label,1000 ml\n\nOld Ezra,whiskey,5000 ml\n\n"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    assert db.check_inventory('Johnnie Walker', 'Black Label')
    assert db.check_inventory('Old Ezra', 'whiskey')
    assert n == 2, n


def test_bulk_load_bottle_types_1():
    db._reset_db()

    data = "Johnnie Walker,Black Label,blended scotch"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)

    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    assert n == 1, n
    
def test_bulk_load_bottle_types_2():
    '''Make sure comments are skipped'''
    db._reset_db()

    data = "#Johnnie Walker,Black Label,blended scotch"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)

    assert not db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    assert n == 0, n
    
def test_bulk_load_bottle_types_3():
    '''Make sure extra lines are skipped'''
    db._reset_db()

    data = "\nJohnnie Walker,Black Label,blended scotch\nOld Ezra,whiskey,whiskey\n"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)

    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    assert db._check_bottle_type_exists('Old Ezra', 'whiskey')
    assert n == 2, n

def test_script_load_bottle_types_1():
    scriptpath = 'bin/load-liquor-types'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-1.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code
    
def test_script_load_inventory_1():

    scriptpath = 'bin/load-liquor-inventory'
    module = imp.load_source('lli', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-1.txt',
    'test-data/inventory-data-1.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code
    
def test_get_liquor_inventory():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

    x = []
    for mfg, liquor in db.get_liquor_inventory():
        x.append((mfg, liquor))

    assert x == [('Johnnie Walker', 'Black Label')], x
