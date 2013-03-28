#! /usr/bin/env python

import os
import db
import recipes

	

def get_index_text():
	index_text = """<html>
<head>
<title>TH1s p4Ge iz sweet</title>
<style type='text/css'>
h1 {color:red;}
body {
font-size: 14px;
}
</style>
<h1>L00K 4T My Aw3s0m3 Dr1nKz!1!1!</h1>
<p><a href='recipes'>My Recipes</a>
<p><a href='inventory'>My Inventory</a>
<p><a href='liquor-types'>My Liquor Typez</a>
<p><a href='converter'>A Converter</a>
<script>
function myFunction()
{
alert("Because he java-scRIPPED his pants"
);
}
</script>
</head>

<p>
<input type="button" onclick="myFunction()" value="Why did Titus Brown blush?"/>
<body>
"""

	return index_text
	
def construct_recipes():
	
	recipes = db.get_all_recipes()
	recipes_str = """<head>
<title>Recipes Page</title>
<style type='text/css'>
h1 {color:red;}
body {
font-size: 14px;
}
</style>
<h1>Recipes</h1>\n\n<body><ul>\n\n"""
	
	for recipe in recipes:
		print "HELLO"
		recipe_html = recipe.get_html_str()
		recipes_str += "<li>" + recipe_html + "</li>\n"
	
	recipes_str += "</ul></body>"
	
	return recipes_str
	

	
def construct_inventory():
		
	inv_str = """<head>
<title>Inventory Page</title>
<style type='text/css'>
h1 {color:red;}
body {
font-size: 14px;
}
</style>
<h1>Inventory</h1>\n\n<body><table>\n """
	
	for item in db.get_liquor_inventory():
		mfg = item[0]
		l = item[1]
		amount = db.get_liquor_amount(mfg,l)
		inv_str += '<tr>\n' + '<td>' +  mfg + '</td>\n'
		inv_str += '  <td>:  ' + l + '      </td>\n'
		inv_str += '  <td>:<i>      ' + str(amount) + ' ml </i> </td>\n </tr>\n'
	
	inv_str += "</body>"
	return inv_str



def construct_liqour_types():

	typ_str = """<head>
<title>Liquor Types</title>
<style type='text/css'>
h1 {color:red;}
body {
font-size: 14px;
}
</style><h1>Liquor Types</h1>\n<body><ul>\n\n"""
	for mfg, liquor in db.get_liquor_inventory():
		typ_str += '<li>' +  '<b>%s</b>  \t  <i>%s</i>' % (mfg, liquor) + '</li>\n'
	
	typ_str += '</ul></body>'
	
	return typ_str
	
def construct_converter_form():
	
	return """<head>
<title>Converter Page</title>
<style type='text/css'>
h1 {color:red;}
body {
font-size: 14px;
}
</style>
<h1>Converter</h1>

<body>
<form action='recv'>
Give an amount <input type='text' name='Amount' size'20'>
<input type='submit'>
</form>
</body>
"""

	
	