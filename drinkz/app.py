#! /usr/bin/env python
from wsgiref.simple_server import make_server
import urlparse
import simplejson
import html_constructor
import db
import recipes
from recipes import Recipe as Recipe




dispatch = {
    '/' : 'index',
    '/recipes' : 'recipes',
    '/inventory' : 'inventory',
    '/liquor-types' : 'types',
    '/converter' : 'form',
    '/recv' : 'recv',
    '/rpc'  : 'dispatch_rpc'
}

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
        data = html_constructor.get_index_text()
        start_response('200 OK', list(html_headers))
        return [data]
        
    def recipes(self, environ, start_response):
        content_type = 'text/html'
        data = html_constructor.construct_recipes()

        print data
        start_response('200 OK', list(html_headers))
        return [data]

    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = "shit's on fire, yo"
       
        start_response('200 OK', list(html_headers))
        return [data]
        
    def inventory(self, environ, start_response):
        content_type = 'text/html'
        data = html_constructor.construct_inventory()
        
        print data
        start_response('200 OK', list(html_headers))
        return [data]
    def types(self, environ, start_response):
        content_type = 'text/html'
        data = html_constructor.construct_liqour_types()
        
        print data
        start_response('200 OK', list(html_headers))
        return [data]


    def helmet(self, environ, start_response):
        content_type = 'image/gif'
        data = open('Spartan-helmet-Black-150-pxls.gif', 'rb').read()

        start_response('200 OK', [('Content-type', content_type)])
        return [data]

    def form(self, environ, start_response):
        content_type = 'text/html'
        data = html_constructor.construct_converter_form()
        
        start_response('200 OK', list(html_headers))
        return [data]
   
    def recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        amount = results['Amount'][0]
        
        amount = str(db.convert_to_ml(amount))

        content_type = 'text/html'
        if amount == '-1':
            data = "What the hell is a %s? <p><a href='./'>Homeward Bound</a>" % (results['Amount'][0].split()[1])
        else:
            data = "Amount: %s ml <p><a href='./'>Homeward Bound</a>" % (amount)

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

    def rpc_hello(self):
        return 'world!'

    def rpc_add(self, a, b):
        return int(a) + int(b)
        
    def rpc_convert_units_to_ml(self, amount):
        """given a str amount, returns ml"""
        
        return db.convert_to_ml(amount)
        

    def rpc_get_recipe_names(self):
       """get_recipe_names() - returns a list of all recipe names"""
       recipes = db.get_all_recipes()
       result = []
       for recipe in recipes:
           print recipe
           result.append(str(recipe))
           
       return result
       
    def rpc_get_liquor_inventory(self):
       """ returns a list of (mfg, liquor) tuples."""
       
       result = []
       
       for (m, l) in db.get_liquor_inventory():
           result.append((m,l))

       return result
       
    def rpc_load_data(self):
        db.load_db('/db')
    

if __name__ == '__main__':
    import random, socket
    port = random.randint(8000, 9999)

    app = SimpleApp()
    app.load_data()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()
