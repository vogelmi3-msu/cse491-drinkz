
#! /usr/bin/env python
from wsgiref.simple_server import make_server
import generate_html
import urlparse
import simplejson
import db
import recipes

import os
import sys
import os.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

dispatch = {
    '/' : 'index',
    '/index.html' : 'index',
    '/error' : 'error',
    '/recipes.html' : 'recipes',
    '/inventory.html' : 'inventory',
    '/liquor_types.html' : 'liquorTypes',
    '/recipes_that_can_be_made_html' : 'producable_recipes',
    '/convert_all_the_things_form': 'convert_all_the_things_form',
    '/convert_all_the_things_recv' : 'convert_all_the_things_recv',
    '/add_liquor_type_form': 'add_liquor_type_form',
    '/add_liquor_type_recv': 'add_liquor_type_recv',
    '/add_to_inventory_form': 'add_to_inventory_form',
    '/add_to_inventory_recv': 'add_to_inventory_recv',
    '/add_a_new_recipe_form': 'add_a_new_recipe_form',
    '/add_a_new_recipe_recv': 'add_a_new_recipe_recv',
    '/rpc'  : 'dispatch_rpc',
    '/view_image.html' : 'view_image'


}

html_headers = [('Content-type', 'text/html')]

class SimpleApp(object):
    def __call__(self, environ, start_response):

        #load from file
        
        generate_html.create_data('bin/sample_database') # in bin/run-web now (comment out??)

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

    def producable_recipes(self, environ, start_response):
        data = generate_html.generate_recipes_that_can_be_made_html()
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
        data = generate_html.convert_all_the_things_form()
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
        
        data += generate_html.generate_menu()
        data += """
</body>
</html>
"""
        start_response('200 OK', list(html_headers))
        return [data]

    def add_liquor_type_form(self, environ, start_response):
        data = generate_html.add_liquor_type_form()
        start_response('200 OK', list(html_headers))
        return [data]
   
    def add_liquor_type_recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)
        mfg = results['mfg'][0]
        liquor = results['liquor'][0]
        typ = results['typ'][0]
        db.add_bottle_type(mfg, liquor, typ)
        db.save_db('bin/sample_database')
        taste_of_success = db._check_bottle_type_exists(mfg, liquor)
        if taste_of_success == True:
            data = generate_html.generate_liquor_types_html()

        else:
            content_type = 'text/html'
            data = """  <html>
    <head>
    <title>Failure to Add Liquor!</title>
        <style type ="text/css">
        h1{color:red;}
    </style>
    </head>
    <body>"""
            data += """Failed to add Liquor type, please try again!"""
            data += generate_html.generate_menu()
            data += """
</body>
</html>
"""     
        start_response('200 OK', list(html_headers))
        return [data]


    def add_to_inventory_form(self, environ, start_response):
        data = generate_html.add_to_inventory_form()
        start_response('200 OK', list(html_headers))
        return [data]
   
    def add_to_inventory_recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        mfg = results['mfg'][0]
        liquor = results['liquor'][0]
        amount = results['amount'][0]
        myBool = db.check_inventory(mfg,liquor)
        if myBool == True:
            intial_amt = db.get_liquor_amount(mfg,liquor)
        else:
            intial_amt = 0
        db.add_to_inventory(mfg, liquor, amount)
        db.save_db('bin/sample_database')
        taste_of_success = db.check_inventory(mfg, liquor)
        amt_success = db.get_liquor_amount(mfg,liquor)
        if taste_of_success == True and amt_success > intial_amt:
            data = generate_html.generate_liquor_types_html()

        else:
            content_type = 'text/html'
            data = """  <html>
    <head>
    <title>Failure to Add Liquor!</title>
        <style type ="text/css">
        h1{color:red;}
    </style>
    </head>
    <body>"""
            data += """Failed to add Liquor type, please try again!"""
            data += generate_html.generate_menu()
            data += """
</body>
</html>
"""     
        start_response('200 OK', list(html_headers))
        return [data]

    def add_a_new_recipe_form(self, environ, start_response):
        print "in add_a_new_recipe_form"
        data = generate_html.add_a_new_recipe_form()
        start_response('200 OK', list(html_headers))
        return [data]
   
    def add_a_new_recipe_recv(self, environ, start_response):
        print "in add_a_new_recipe_recv"
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        name = results['name'][0]
        ings = results['ings'][0]
        indv_ings = ings.split(',')
        ind_list =[]
        for item in indv_ings:
            myTup = tuple(item.split(':'))
            ind_list.append(myTup)
        
        recipe = recipes.Recipe(name,ind_list)
        db.add_recipe(recipe)
        db.save_db('bin/sample_database')
        taste_of_success = db.get_recipe(name)
        if taste_of_success == recipe:
            data = generate_html.generate_recipes_html()
        else:
            content_type = 'text/html'
            data = """  <html>
    <head>
    <title>Failure to add recipe!</title>
        <style type ="text/css">
        h1{color:red;}
    </style>
    </head>
    <body>"""
            data += """Failed to add Recipe, please try again!"""
            data += generate_html.generate_menu()
            data += """
</body>
</html>
"""     
        start_response('200 OK', list(html_headers))
        return [data]

    def view_image(self, environ, start_response):
        content_type = 'image/jpg'
        pth = os.path.dirname(__file__)
        filename = pth + '/searchbyspirit.jpg'
        data = open(filename, 'rb').read()
        start_response('200 OK', [('Content-Type', content_type)])
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

    def rpc_add_recipe(self, name, ingredients):
        r = recipes.Recipe(name,ingredients)
        return db.add_recipe(r)

    def rpc_add_to_inventory(self, mfg,liquor,amt ):
        return db.add_to_inventory(mfg,liquor,amt)

    def rpc_add_bottle_type(self, mfg, liquor,typ):
        return db.add_bottle_type(mfg,liquor,typ)

    def rpc_producable_recipes(self):
        return list(db.recipes_we_can_make())

