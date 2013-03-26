#! /usr/bin/env python

import os
import db
import recipes

	

def get_index_text():
	index_text = """"<b>L00K 4T My Aw3s0m3 Dr1nKz!1!1!</b>
	<p><a href='recipes'>My Recipes</a>
	<p><a href='inventory'>My Inventory</a>
	<p><a href='liquor-types'>My Liquor Typez</a>
	<p><a href='converter'>A Converter</a>"""

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
	
	