#! /usr/bin/env python

import os
from drinkz import db
from drinkz import recipes

def fill_stuff():
	db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
	db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

	db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
	db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')

	db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
	db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

	db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
	db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

	r = recipes.Recipe('scotch on the rocks', [('blended scotch', '4 oz')])
	db.add_recipe(r)

	r = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),('vermouth', '1.5 oz')])
	db.add_recipe(r)

	r = recipes.Recipe('vomit inducing martini', [('orange juice','6 oz'),('vermouth','1.5 oz')])
	db.add_recipe(r)


fill_stuff()   

try:
	os.mkdir('html')
except OSError:
	# already exists
	pass

###

###INDEX
fp = open('html/index.html', 'w')
print >>fp, """"<b>L00K 4T My Aw3s0m3 Dr1nKz!1!1!</b>
<p><a href='recipes.html'>My Recipes</a>"""

print >>fp, """
<p>
<a href='inventory.html'>My Inventory</a>
"""

print >>fp, """
<p>
<a href='liquor_types.html'>My Liquor Typez</a>
"""

fp.close()

###



### RECIPES
recipes = db.get_all_recipes()
rec_fp = open('html/recipes.html', 'w')

recipes_str = "<b>Recipes</b>\n\n<ul>"

for recipe in recipes:
	recipe_html = recipe.get_html_str()
	recipes_str += '<li>' + recipe_html + '</li>\n'

recipes_str+= '</ul>'

print >>rec_fp, recipes_str

rec_fp.close()
###

### INVENTORY

inv_fp = open('html/inventory.html', 'w')

inv_str = "<b>Inventory</b>\n\n<table>\n "

for item in db.get_liquor_inventory():
	mfg = item[0]
	l = item[1]
	amount = db.get_liquor_amount(mfg,l)
	inv_str += '<tr>\n' + '<td>' +  mfg + '</td>\n'
	inv_str += '  <td>:  ' + l + '      </td>\n'
	inv_str += '  <td>:<i>      ' + str(amount) + ' ml </i> </td>\n </tr>\n'

print >>inv_fp, inv_str
inv_fp.close()

###

### Liquor Types

typ_fp = open('html/liquor_types.html', 'w')
typ_str = "<b>Liquor Types</b>\n<ul>\n\n"
for mfg, liquor in db.get_liquor_inventory():
	typ_str += '<li>' +  '<b>%s</b>  \t  <i>%s</i>' % (mfg, liquor) + '</li>\n'

typ_str += '</ul>'

print >>typ_fp, typ_str

typ_fp.close()

###


