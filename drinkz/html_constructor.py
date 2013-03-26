#! /usr/bin/env python

import os
import db
import recipes

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
	

def get_index_text():
	index_text = """"<b>L00K 4T My Aw3s0m3 Dr1nKz!1!1!</b>
	<p><a href='recipes.html'>My Recipes</a>
	<p><a href='recipes.html'>My Recipes</a>
	<p><a href='inventory.html'>My Inventory</a>
	<p><a href='liquor_types.html'>My Liquor Typez</a>"""

	return index_text
	
def construct_recipes():
	
	recipes = db.get_all_recipes()
	recipes_str = "<b>Recipes</b>\n\n<ul>\n\n"
	
	for recipe in recipes:
		print "HELLO"
		recipe_html = recipe.get_html_str()
		recipes_str += "<li>" + recipe_html + "</li>\n"
	
	recipes_str += "</ul>"
	
	return recipes_str
	

	
def construct_inventory():
		
	inv_str = "<b>Inventory</b>\n\n<table>\n "
	
	for item in db.get_liquor_inventory():
		mfg = item[0]
		l = item[1]
		amount = db.get_liquor_amount(mfg,l)
		inv_str += '<tr>\n' + '<td>' +  mfg + '</td>\n'
		inv_str += '  <td>:  ' + l + '      </td>\n'
		inv_str += '  <td>:<i>      ' + str(amount) + ' ml </i> </td>\n </tr>\n'
	
	return inv_str



def construct_liqour_types():

	typ_str = "<b>Liquor Types</b>\n<ul>\n\n"
	for mfg, liquor in db.get_liquor_inventory():
		typ_str += '<li>' +  '<b>%s</b>  \t  <i>%s</i>' % (mfg, liquor) + '</li>\n'
	
	typ_str += '</ul>'
	
	return typ_str
	
	