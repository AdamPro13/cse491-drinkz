#!/usr/bin/env python

import urlparse
import random
import socket
import uuid
from os import path

import simplejson
import jinja2
from wsgiref.simple_server import make_server
from Cookie import SimpleCookie

import db
from db import load_db
import recipes

usernames = {}

dispatch = {
    '/' : 'login1',
    '/index':'index',
    '/recipesList' : 'recipesList',
    '/inventoryList' : 'inventoryList',
    '/liqourTypes' : 'liqourTypes',
    '/convertToML' : 'formConvertToML',
    '/recvAmount' : 'recvAmount',
    '/addType' : 'addType',
    '/addInventory' : 'addInventory',
    '/addRecipe' : 'addRecipe',
    '/addSong' : 'addSong',
    '/login_1' : 'login1',
    '/login1_process' : 'login1_process',
    '/logout' : 'logout',
    '/status' : 'status',
    '/rpc' : 'dispatch_rpc',
    '/jquery.js': 'jquery'
}

base_dir = path.realpath(path.dirname(path.realpath(__file__)) + '/../')
html_headers = [('Content-type', 'text/html')]

class SimpleApp(object):
    def __call__(self, environ, start_response):
        
        path = environ['PATH_INFO']
        
        fn_name = dispatch.get(path, 'error')
        
        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to
        # the 'path'.
        fn = getattr(self, fn_name, None)
        
        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s found" % path]
        
        return fn(environ, start_response)
    
    def index(self, environ, start_response):
        name1 = ''
        name1_key = '*empty*'
        if 'HTTP_COOKIE' in environ:
            c = SimpleCookie(environ.get('HTTP_COOKIE', ''))
            if 'name1' in c:
                key = c.get('name1').value
                name1 = usernames.get(key, '')
                name1_key = key
        if name1=='':
            return self.login1(environ,start_response)
        data = """\
<html>
<head>
<title>Home</title>
<style type='text/css'>
h1 {color:red;}
body {
font-size: 17px;
}
</style>
<script>
function myFunction()
{
alert("Hello! I am an alert box!");
}
</script>
</script>
<h1>Drinkz Home</h1>
Visit:
<a href='recipesList'>Recipes</a>,
<a href='inventoryList'>Inventory</a>,
<a href='liqourTypes'>Liqour Types</a>,
<a href='convertToML'>Convert to ml</a>
<a href='logout'>Log Out</a>
<p>
<input type="button" onclick="myFunction()" value="Show alert box" />
</head>
<body>

"""
        start_response('200 OK', list(html_headers))
        return [data]

    def login1(self, environ, start_response):
        name1 = ''
        name1_key = '*empty*'
        if 'HTTP_COOKIE' in environ:
            c = SimpleCookie(environ.get('HTTP_COOKIE', ''))
            if 'name1' in c:
                key = c.get('name1').value
                name1 = usernames.get(key, '')
                name1_key = key
        if name1:
            return self.index(environ,start_response)
        else:
            start_response('200 OK', list(html_headers))
            title = 'login'
            loader = jinja2.FileSystemLoader('../drinkz/templates')
            env = jinja2.Environment(loader=loader)
            template = env.get_template('login1.html')
            return str(template.render(locals()))

    def login1_process(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
        
        name = results['name'][0]
        content_type = 'text/html'
        
        # authentication would go here -- is this a valid username/password,
        # for example?
        
        k = str(uuid.uuid4())
        usernames[k] = name
        
        headers = list(html_headers)
        headers.append(('Location', '/index'))
        headers.append(('Set-Cookie', 'name1=%s' % k))
        
        start_response('302 Found', headers)
        return ["Redirect to /index..."]
    
    def logout(self, environ, start_response):
        if 'HTTP_COOKIE' in environ:
            c = SimpleCookie(environ.get('HTTP_COOKIE', ''))
            if 'name1' in c:
                key = c.get('name1').value
                name1_key = key
                
                if key in usernames:
                    del usernames[key]
                    print 'DELETING'
        
        pair = ('Set-Cookie',
                'name1=deleted; Expires=Thu, 01-Jan-1970 00:00:01 GMT;')
        headers = list(html_headers)
        headers.append(('Location', '/status'))
        headers.append(pair)
        
        start_response('302 Found', headers)
        return ["Redirect to /status..."]
    
    def status(self, environ, start_response):
        start_response('200 OK', list(html_headers))
        
        name1 = ''
        name1_key = '*empty*'
        if 'HTTP_COOKIE' in environ:
            c = SimpleCookie(environ.get('HTTP_COOKIE', ''))
            if 'name1' in c:
                key = c.get('name1').value
                name1 = usernames.get(key, '')
                name1_key = key
        
        title = 'login status'
        loader = jinja2.FileSystemLoader('../drinkz/templates')
        env = jinja2.Environment(loader=loader)
        template = env.get_template('status.html')
        return str(template.render(locals()))
    
    def recipesList(self, environ, start_response):
        data = recipesList()
        start_response('200 OK', list(html_headers))
        return [data]
    
    def inventoryList(self, environ, start_response):
        data = inventoryList()
        start_response('200 OK', list(html_headers))
        return [data]
    
    def liqourTypes(self, environ, start_response):
        data = liqourTypesList()
        start_response('200 OK', list(html_headers))
        return [data]
    
    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
        
        start_response('200 OK', list(html_headers))
        return [data]

    def formConvertToML(self, environ, start_response):
        content_type = 'text/html'
        data = open('../drinkz/somefile.html').read()
        
        start_response('200 OK', list(html_headers))
        return [data]
    
    
    def recvAmount(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
        
        amount = results['amount'][0]
        
        amount = str(db.convert_to_ml(amount))
        
        
        content_type = 'text/html'
        data = "Converted Amount %s ml<p><a href='./'>return to index</a>" % (amount)
        
        start_response('200 OK', list(html_headers))
        return [data]
    
    def jquery(self, environ, start_response):
        data = open(base_dir + '/js/jquery.js').read()
        start_response('200 OK', [('Content-Type', 'text/javascript')])
        return [data]
    
    def addType(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
        mfg = results['mfg'][0]
        liquor = results['liquor'][0]
        typ = results['typ'][0]
        db.add_bottle_type(mfg, liquor, typ)
        
        
        content_type = 'text/html'
        data = liqourTypesList();
        start_response('200 OK', list(html_headers))
        return [data]
    
    def addInventory(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
        mfg = results['mfg'][0]
        liquor = results['liquor'][0]
        amt = results['amt'][0]
        try:
            db.add_to_inventory(mfg, liquor, amt)
            data = inventoryList()
        except Exception:
            data = inventoryList() +"""<script>
                
                alert("That liquor is not an added type.");
                
                </script>"""
        
        content_type = 'text/html'
        start_response('200 OK', list(html_headers))
        return [data]

    def addRecipe(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
        name = results['name'][0]
        ings = results['ing'][0]
        myList = ings.split(',')
        myIngSet = set()
        i = 0
        while i < len(myList):
            
            val = (ingred,amount) = (myList[i],myList[i+1])
            myIngSet.add(val)
            i+=2
        
        r = recipes.Recipe(name,myIngSet)
        try:
            db.add_recipe(r)
            data = recipesList()
        except Exception:
            data = recipesList()

        content_type = 'text/html'
        start_response('200 OK', list(html_headers))
        return [data]

    def dispatch_rpc(self, environ, start_response):
        # POST requests deliver input data via a file-like handle,
        # with the size of the data specified by CONTENT_LENGTH;
        # see the WSGI PEP.
        
        if environ['REQUEST_METHOD'].endswith('POST'):
            body = None
            if environ.get('CONTENT_LENGTH'):
                length = int(environ['CONTENT_LENGTH'])
                body = environ['wsgi.input'].read(length)
                response = self._dispatch(body) + '\n'
                start_response('200 OK', [('Content-Type', 'application/json')])
                
                return [response]
        
        # default to a non JSON-RPC error.
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
        
        start_response('200 OK', list(html_headers))
        return [data]
    
    def _decode(self, json):
        return simplejson.loads(json)
    
    def _dispatch(self, json):
        rpc_request = self._decode(json)
        
        method = rpc_request['method']
        params = rpc_request['params']
        
        rpc_fn_name = 'rpc_' + method
        fn = getattr(self, rpc_fn_name)
        result = fn(*params)
        
        response = { 'result' : result, 'error' : None, 'id' : 1 }
        response = simplejson.dumps(response)
        return str(response)
    
    def rpc_convert_units_to_ml(self,amount):
        return str(db.convert_to_ml(amount))
    def rpc_get_recipe_names(self):
        recipeList = db.get_all_recipes()
        nameList = list()
        for recipe in recipeList:
            nameList.append(recipe._recipeName)
        return nameList
    def rpc_get_liqour_inventory(self):
        liqourInvList = list()
        for (m,l) in db.get_liquor_inventory():
            liqourInvList.append((m,l))
        return liqourInvList
    def rpc_get_liqour_types(self):
        liqourTypeList = list()
        for (m,l) in db.get_liquor_types():
            liqourTypeList.append((m,l))
        return liqourTypeList
    
    def rpc_add_bottle_type(self,mfg,liquor,typ):
        returnVal = False
        try:
            db.add_bottle_type(mfg, liquor, typ)
            returnVal = True;
        except Exception:
            returnVal = False
        return returnVal

    def rpc_add_to_inventory(self,mfg,liquor,amount):
        returnVal = False
        try:
            db.add_to_inventory(mfg, liquor, amount)
            returnVal = True;
        except Exception:
            returnVal = False
        return returnVal

    def rpc_add_recipe(self,name,ings):
        myList = ings.split(',')
        myIngSet = set()
        i = 0
        while i < len(myList):
            
            val = (ingred,amount) = (myList[i],myList[i+1])
            myIngSet.add(val)
            i+=2
        
        r = recipes.Recipe(name,myIngSet)
        try:
            db.add_recipe(r)
            returnVal = True
        except Exception:
            returnVal = False
        return returnVal

    def rpc_hello(self):
        return 'world!'
    
    def rpc_add(self, a, b):
        return int(a) + int(b)

def recipesList():
    # this sets up jinja2 to load templates from the 'templates' directory
    loader = jinja2.FileSystemLoader('../drinkz/templates')
    env = jinja2.Environment(loader=loader)
    
    # pick up a filename to render
    filename = "listPages.html"    #recipe nonsense
    recipeList = db.get_all_recipes()
    recipeNameList = list()
    for recipe in recipeList:
        if recipe.need_ingredients():
            val = "no"
        else:
            val = "yes"
        recipeNameList.append(recipe._recipeName + " " + val)

    
    # variables for the template rendering engine
    
    vars = dict(title = 'Recipe List', addtitle = "Add Recipe",
                form = """<form action='addRecipe'>
                    Name<input type='text' name='name' size'20'>
                    Ingredients i.e.-'vodka,4 oz,orange juice,12 oz'<input type='text' name='ing' size'20'>
                    <input type='submit'>
                    </form>""", names=recipeNameList)
    
    
    try:
        template = env.get_template(filename)
    except Exception:# for nosetests
        loader = jinja2.FileSystemLoader('./drinkz/templates')
        env = jinja2.Environment(loader=loader)
        template = env.get_template(filename)


    x = template.render(vars).encode('ascii','ignore')
    return x
def inventoryList():
    # this sets up jinja2 to load templates from the 'templates' directory
    loader = jinja2.FileSystemLoader('../drinkz/templates')
    env = jinja2.Environment(loader=loader)
    
    # pick up a filename to render
    filename = "listPages.html"
    
    #recipe nonsense
    inventoryList = list()
    for (m,l) in db.get_liquor_inventory():
        inventoryList.append(str(m)+ " " + str(l)+ " "  + str(db.get_liquor_amount(m,l))+" ml")
    
    
    # variables for the template rendering engine
    
    vars = dict(title = 'Inventory List', addtitle = "Add to Inventory",
                form = """<form action='addInventory'>
Manufacturer<input type='text' name='mfg' size'20'>
Liquor<input type='text' name='liquor' size'20'>
Amount<input type='text' name='amt' size'20'><p>
<input type='submit'>
</form>""", names=inventoryList)
    
    template = env.get_template(filename)
    
    x = template.render(vars).encode('ascii','ignore')
    return x

def liqourTypesList():
    # this sets up jinja2 to load templates from the 'templates' directory
    
    loader = jinja2.FileSystemLoader('../drinkz/templates')
    env = jinja2.Environment(loader=loader)
    
    # pick up a filename to render
    filename = "listPages.html"
    
    #recipe nonsense
    liqourTypesList = list()
    for (m,l) in db.get_liquor_types():
        liqourTypesList.append(str(m)+ " " + str(l))
    
    
    # variables for the template rendering engine
    
    vars = dict(title = 'Liquor Types List', addtitle = "Add Liquor Type",
                form = """<form action='addType'>
Manufacturer<input type='text' name='mfg' size'20'>
Liquor<input type='text' name='liquor' size'20'>
Generic Type<input type='text' name='typ' size'20'><p>
<input type='submit'>
</form>""", names=liqourTypesList)

    template = env.get_template(filename)
    
    x = template.render(vars).encode('ascii','ignore')    
    return x

def setUpWebServer():
    filename = 'database.db'
    load_db(filename)
    port = random.randint(8000, 9999)
    
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
        (socket.getfqdn(), port)
    httpd.serve_forever()
