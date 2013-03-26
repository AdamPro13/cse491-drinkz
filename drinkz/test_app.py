import app
import urllib
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

fill_stuff()

def test_index():
	environ = {}
	environ['PATH_INFO'] = '/'
	
	d = {}
	def my_start_response(s, h, return_in=d):
		d['status'] = s
		d['headers'] = h

	app_obj = app.SimpleApp()
	results = app_obj(environ, my_start_response)

	text = "".join(results)
	status, headers = d['status'], d['headers']

	assert text.find('L00K 4T My Aw3s0m3 Dr1nKz!1!1!') != -1, text
	assert ('Content-type', 'text/html') in headers
	assert status == '200 OK'
	
def test_recipes():
	environ = {}
	environ['PATH_INFO'] = '/recipes'
	
	d = {}
	def my_start_response(s, h, return_in=d):
		d['status'] = s
		d['headers'] = h
	
	app_obj = app.SimpleApp()
	results = app_obj(environ, my_start_response)
	
	text = "".join(results)
	status, headers = d['status'], d['headers']
	
	assert text.find('<li><b>scotch on the rocks</b>:  blended scotch- <i>4 oz</i>		<b>NO</b></li>') != -1, text
	assert ('Content-type', 'text/html') in headers
	assert status == '200 OK'
	
def test_inventory():
	environ = {}
	environ['PATH_INFO'] = '/inventory'
	
	d = {}
	def my_start_response(s, h, return_in=d):
		d['status'] = s
		d['headers'] = h
	
	app_obj = app.SimpleApp()
	results = app_obj(environ, my_start_response)
	
	text = "".join(results)
	status, headers = d['status'], d['headers']
	
	assert text.find("<td>Johnnie Walker</td>") != -1, text
	assert ('Content-type', 'text/html') in headers
	assert status == '200 OK'

def test_types():
	environ = {}
	environ['PATH_INFO'] = '/liquor-types'

	d = {}
	def my_start_response(s, h, return_in=d):
		d['status'] = s
		d['headers'] = h

	app_obj = app.SimpleApp()
	results = app_obj(environ, my_start_response)

	text = "".join(results)
	status, headers = d['status'], d['headers']

	assert text.find("<li><b>Johnnie Walker</b>  	  <i>black label</i></li>") != -1, text
	assert ('Content-type', 'text/html') in headers
	assert status == '200 OK'



def test_form_recv():
	environ = {}
	environ['QUERY_STRING'] = urllib.urlencode(dict(Amount='100 ml'))
	environ['PATH_INFO'] = '/recv'

	d = {}
	def my_start_response(s, h, return_in=d):
		d['status'] = s
		d['headers'] = h

	app_obj = app.SimpleApp()
	results = app_obj(environ, my_start_response)

	text = "".join(results)
	status = d['status']
	headers = d['headers']

	assert text.find("Amount: 100.0 ml") != -1, text
	assert ('Content-type', 'text/html') in headers
	assert status == '200 OK'

