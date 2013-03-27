
#! /usr/bin/env python

import generate_html
import urlparse
import simplejson

dispatch = {
    '/' : 'index',
    '/content' : 'somefile',
    '/error' : 'error',
    '/recipes' : 'recipes',
    '/inventory' : 'inventory',
    '/liquorTypes' : 'liquorTypes'
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
        data = generate_index_html()
        start_response('200 OK', list(html_headers))
        return [data]
        
    def recipes(self, environ, start_response):
        data = generate_recipes_html()
        start_response('200 OK', list(html_headers))
        return [data]

    def inventory(self, environ, start_response):
        data = generate_inventory_html()
        start_response('200 OK', list(html_headers))
        return [data]

    def liquorTypes(self, environ, start_response):
        data = generate_liquor_types_html()
        start_response('200 OK', list(html_headers))
        return [data]

    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]


    def form(self, environ, start_response):
        data = form()

        start_response('200 OK', list(html_headers))
        return [data]
   
    def recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        firstname = results['firstname'][0]
        lastname = results['lastname'][0]

        content_type = 'text/html'
        data = "First name: %s; last name: %s.  <a href='./'>return to index</a>" % (firstname, lastname)

        start_response('200 OK', list(html_headers))
        return [data]

    def convert_all_the_things_form(self, environ, start_response):
        data = convert_all_the_things_form()

        start_response('200 OK', list(html_headers))
        return [data]
   
    def convert_all_the_things_recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        firstname = results['firstname'][0]
        lastname = results['lastname'][0]

        content_type = 'text/html'
        data = "First name: %s; last name: %s.  <a href='./'>return to index</a>" % (firstname, lastname)

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
    #header, footer = generate_html.load_header_footer()
    # data =  """\
    # <div class="row-fluid">
    #     <div class="span8">
    #         <form class="form-horizontal" action="/recv_conversion">
    #             <div class="control-group">
    #                 <label for="amount" class="control-label">Amount of Liquid:</label>
    #                 <div class="controls">
    #                     <input type="text" name="amount" id="amount" size="20">
    #                 </div>
    #             </div>

    #             <div class="control-group">
    #                 <label for="unit" class="control-label">Unit:</label>
    #                 <div class="controls">
    #                     <select name="unit" id="unit">
    #                         <option value="oz">oz</option>
    #                         <option value="gallon">gallons</option>
    #                         <option value="liter">liters</option>
    #                     </select>
    #                 </div>
    #             </div>

    #             <div class="control-group">
    #                 <div class="controls">
    #                     <button type="submit" class="btn btn-primary">Submit</button>
    #                 </div>
    #             </div>
    #         </form>
    #     </div>
    # </div>
    # """

    # return data
        return """
<form action='recv'>
Input the volume and units? <input type='text' name='firstname' size'20'>
<input type='submit'>
</form>
"""

def convert_all_the_things_result(amount, unit, amount_converted):
   # header, footer = generate_html.load_header_footer()
    amount_entered = "<h2>Amount Entered: %s %s</h2>" % (amount, unit)
    amount_converted = "<h2>Amount Converted: %.2f mL</h2>" % amount_converted
    data = """\
    <div class="row-fluid">
        <div class="hero-unit">
    """
    data += amount_entered
    data += amount_converted
    data += """\
            <p><a href="/" class="btn btn-primary btn-large" style="margin-top: 2em;">Return to Home</a></p>
        </div>
    </div>
    """

    return header + data + footer
