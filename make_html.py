#! /usr/bin/env python

import os
from drinkz import db
from drinkz import recipes
from drinkz import html_constructor


db.load_db('bin/db')


try:
	os.mkdir('html')
except OSError:
	# already exists
	pass

###

###INDEX
fp = open('html/index.html', 'w')

index_text = html_constructor.get_index_text()


print >> fp, index_text

fp.close()

###



### RECIPES
recipes = db.get_all_recipes()
rec_fp = open('html/recipes.html', 'w')

recipes_str = html_constructor.construct_recipes()
print >>rec_fp, recipes_str

rec_fp.close()
###

### INVENTORY

inv_fp = open('html/inventory.html', 'w')

inv_str = html_constructor.construct_inventory()

print >>inv_fp, inv_str
inv_fp.close()

###

### Liquor Types

typ_fp = open('html/liquor_types.html', 'w')
typ_str = html_constructor.construct_liqour_types()
print >>typ_fp, typ_str

typ_fp.close()

###


