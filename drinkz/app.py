
#! /usr/bin/env python
from wsgiref.simple_server import make_server
import generate_html
import urlparse
import json as simplejson
import db

dispatch = {
    '/' : 'index',
    '/index.html' : 'index',
    '/content' : 'somefile',
    '/error' : 'error',
    '/recipes.html' : 'recipes',
    '/inventory.html' : 'inventory',
    '/liquor_types.html' : 'liquorTypes',
    '/recv' : 'recv',
    '/form' : 'form',
    '/convert_all_the_things_form': 'convert_all_the_things_form',
    '/convert_all_the_things_recv' : 'convert_all_the_things_recv'
}

html_headers = [('Content-type', 'text/html')]

class SimpleApp(object):
    def __call__(self, environ, start_response):

        generate_html.create_data()
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
        data = generate_html.generate_index_html()
        start_response('200 OK', list(html_headers))
        return [data]
        
    def recipes(self, environ, start_response):
        data = generate_html.generate_recipes_html()
        start_response('200 OK', list(html_headers))
        return [data]

    def inventory(self, environ, start_response):
        data = generate_html.generate_inventory_html()
        start_response('200 OK', list(html_headers))
        return [data]

    def liquorTypes(self, environ, start_response):
        data = generate_html.generate_liquor_types_html()
        start_response('200 OK', list(html_headers))
        return [data]

    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def convert_all_the_things_form(self, environ, start_response):
        data = convert_all_the_things_form()
        start_response('200 OK', list(html_headers))
        return [data]
   
    def convert_all_the_things_recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        amount_to_convert = results['InputAmt'][0]
        converted_amt = db.convert_to_ml(amount_to_convert)
        content_type = 'text/html'
        data = """  <html>
    <head>
    <title>Converted!</title>
        <style type ="text/css">
        h1{color:red;}
    </style>
    </head>
    <body>"""
        data += """<h1> Converted! </h1> <p>Amount to Convert: %s; Converted volume: %s mL. </p>""" % (amount_to_convert, converted_amt)
        data += """<p>
<a href = 'convert_all_the_things_form'>Convert another volume?</a>
</p>
<p> 
<a href='index.html'>Home</a>
</p>
<p>
<a href = 'recipes.html'>Recipes</a>
</p>
<p>
<a href = 'liquor_types.html'>Liquor Types</a>
</p>
<p>
<a href = 'inventory.html'>Inventory</a>
</p>
</body>
</html>
"""
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

def convert_all_the_things_form():
        return """  <html>
    <head>
    <title>Convert!</title>
        <style type ="text/css">
        h1{color:red;}
    </style>
    </head>
    <body>
    <h1> Convert!</h1>
<form action='convert_all_the_things_recv'>
Input the volume and units? (oz, gallon, or liter) <input type='text' name='InputAmt' size'20'>
<input type='submit'>
</form>
<p> 
<a href='index.html'>Home</a>
</p>
<p>
<a href = 'recipes.html'>Recipes</a>
</p>
<p>
<a href = 'liquor_types.html'>Liquor Types</a>
</p>
<p>
<a href = 'inventory.html'>Inventory</a>
</p>
</body>
</html>
"""

