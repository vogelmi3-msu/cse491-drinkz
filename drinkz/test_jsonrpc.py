#! /usr/bin/env python
import sys
import simplejson
import urllib2
import db, recipes, app, generate_html
from StringIO import StringIO

#Reference: https://github.com/ctb/cse491-webz/blob/master/json-rpc-client.py
#############################################################################
#Input: jsonrpc method and parameters
#Output: the status, header and result of calling the jsonrpc function based
#	 on given method and parameters
#############################################################################
def call_remote(method, params):
    env = {}
    env['PATH_INFO'] = '/rpc'
    env['REQUEST_METHOD'] = 'POST'
    env['wsgi.input'] = StringIO(simplejson.dumps({
        'method': method,
        'params': params,
        'id': 1
    }))
    env['CONTENT_LENGTH'] = len(env['wsgi.input'].getvalue())

    response = {}
    def my_start_response(s, h, return_in=response):
        response['status'] = s
        response['headers'] = h

    #Create a new SimpleApp object
    app_obj = app.SimpleApp()

    #Get the content
    content = app_obj(env, my_start_response)
    #Get the status
    status = response['status']
    #Get the header
    header = response['headers']
    #Get result
    result =  simplejson.loads(''.join(content))
    #Return: status, header, and result 
    #of calling the jsonrpc function based on given method and parameter
    return (status, header, result)


#############################################################################
#Test function "rpc_add_recipe"
#Passes: scotch on the rocks, ('blended scotch','4 oz')
#Check if recipe name and ingredients are on the database
#############################################################################
def test_rpc_add_recipe():
    db._reset_db()
    name = "sex on the beach (aka scotch on the rocks)"
    ingredients = [('4 oz', 'blended scotch')]
    s, h, result = call_remote('add_recipe', [name,ingredients])

    #Check for valid status
    assert s == '200 OK'

    #Check for correct content
    assert ('Content-Type', 'application/json') in h, h

    #Check for scotch on the rocks
    assert db._check_recipe_exists(name)


#############################################################################
#Test function "rpc_add_to_inventory"
#Passes: manufacturer, liquor, amount 
#Check if added to inventory   
#############################################################################
def test_rpc_add_to_inventory():
    db._reset_db()
    
    #Add bottle type first
    db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
    
    mfg = 'Johnnie Walker'
    liquor =  'black label'
    amt =  '500 ml'

    #originalAmt = db.get_liquor_amount(mfg,liquor)
    s, h, result = call_remote('add_to_inventory', [mfg,liquor,amt])

    #Check for valid status
    assert s == '200 OK'

    #Check for correct content
    assert ('Content-Type', 'application/json') in h, h

    #Check if the data has been added to inventory
    assert db.check_inventory(mfg,liquor)



#############################################################################
#Test function "rpc_add_bottle_type"
#Passes: manufacturer, liquor, type 
#Check if added to bottle_types_db
#############################################################################
def test_rpc_add_bottle_type():
    db._reset_db()
    
    mfg = 'Johnnie Walker'
    liquor =  'black label'
    type =  'blended scotch'

    s, h, result = call_remote('add_bottle_type', [mfg,liquor,type])

    #Check for valid status
    assert s == '200 OK'

    #Check for correct content
    assert ('Content-Type', 'application/json') in h, h

    #Check if the data has been added to bottle type
    assert db._check_bottle_type_exists(mfg,liquor)


