#! /usr/bin/env python
import sys
import simplejson
import urllib2
import app
import StringIO
import db


def test_convert_amount():
	environ = {}
	environ['PATH_INFO'] = '/rpc'
	environ['REQUEST_METHOD'] = 'convert_units_to_mlPOST'

	

	d = dict(method = 'convert_units_to_ml', params=['123 ml'], id=1)
	encoded = simplejson.dumps(d)	
	output = StringIO.StringIO(encoded)

	
	environ['wsgi.input'] = output
	environ['CONTENT_LENGTH'] = len(output.getvalue())
	
	headers = { 'Content-Type' : 'application/json' }

	def my_start_response(s, headers, return_in=d):
		d['status'] = s
		d['headers'] = headers
		

	app_obj = app.SimpleApp()
	json_response = app_obj(environ, my_start_response)
	json_response = json_response[0]
	response = simplejson.loads(json_response)
	
	assert response['result'] == 123.0


def test_get_recipe_names():
	db.load_db('db')
	environ = {}
	environ['PATH_INFO'] = '/rpc'
	environ['REQUEST_METHOD'] = 'get_recipe_namesPOST'



	d = dict(method = 'get_recipe_names', params=[], id=1)
	encoded = simplejson.dumps(d)	
	output = StringIO.StringIO(encoded)


	environ['wsgi.input'] = output
	environ['CONTENT_LENGTH'] = len(output.getvalue())

	headers = { 'Content-Type' : 'application/json' }

	def my_start_response(s, headers, return_in=d):
		d['status'] = s
		d['headers'] = headers


	app_obj = app.SimpleApp()
	json_response = app_obj(environ, my_start_response)
	json_response = json_response[0]
	response = simplejson.loads(json_response)

	assert response['result'][0] == 'scotch on the rocks:  blended scotch- 4 oz'
	
def test_get_liquor_inventory():
	db.load_db('db')
	environ = {}
	environ['PATH_INFO'] = '/rpc'
	environ['REQUEST_METHOD'] = 'get_liquor_inventoryPOST'



	d = dict(method = 'get_liquor_inventory', params=[], id=1)
	encoded = simplejson.dumps(d)	
	output = StringIO.StringIO(encoded)


	environ['wsgi.input'] = output
	environ['CONTENT_LENGTH'] = len(output.getvalue())

	headers = { 'Content-Type' : 'application/json' }

	def my_start_response(s, headers, return_in=d):
		d['status'] = s
		d['headers'] = headers


	app_obj = app.SimpleApp()
	json_response = app_obj(environ, my_start_response)
	json_response = json_response[0]
	response = simplejson.loads(json_response)


	assert response['result'][0] == ['Johnnie Walker', 'black label']

