#! /usr/bin/env python
from wsgiref.simple_server import make_server
import urlparse
import simplejson
import html_constructor
import db

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
        print path

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
        data = form()
        
        start_response('200 OK', list(html_headers))
        return [data]
   
    def recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        amount = results['Amount'][0]
        
        amount = str(db.convert_to_ml(amount))

        content_type = 'text/html'
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
    
def form():
    return """
<form action='recv'>
Give an amount <input type='text' name='Amount' size'20'>
<input type='submit'>
</form>
"""

if __name__ == '__main__':
    import random, socket
    port = random.randint(8000, 9999)
    
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()
