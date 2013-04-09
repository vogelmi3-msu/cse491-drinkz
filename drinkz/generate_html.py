#from drinkz
import db
import recipes
import os

try:
	os.mkdir('html')
except OSError:
	pass

try:
	os.mkdir('html/subdir')
except OSError:
	pass



########################################################################
#Add items to the inventory
#Copied the drinks from drinkz/test_recipes.py
########################################################################



def create_data():
	try:
		drinkz.db.load_db('database')
	except Exception:
		db._reset_db()

		db.add_bottle_type('Johnnie Walker', 'black label', 'blended scotch')
		db.add_to_inventory('Johnnie Walker', 'black label', '1 gallon')
		db.add_to_inventory('Johnnie Walker', 'black label', '500 ml')

		db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
		db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')

		db.add_bottle_type('Gray Goose', 'vodka', 'unflavored vodka')
		db.add_to_inventory('Gray Goose', 'vodka', '1 liter')

		db.add_bottle_type('Rossi', 'extra dry vermouth', 'vermouth')
		db.add_to_inventory('Rossi', 'extra dry vermouth', '24 oz')

		db.add_bottle_type('Jose Cuervo', 'Silver', 'tequila')
		db.add_to_inventory('Jose Cuervo', 'Silver', '1 liter')

		r = recipes.Recipe('scotch on the rocks', [('blended scotch','4 oz')])
		db.add_recipe(r)
		r = recipes.Recipe('vodka martini', [('unflavored vodka', '6 oz'),('vermouth', '1.5 oz')])
		db.add_recipe(r)
		r = recipes.Recipe('vomit inducing martini', [('orange juice','6 oz'),('vermouth','1.5 oz')])
		db.add_recipe(r)
		r = recipes.Recipe('whiskey bath', [('blended scotch', '2 liter')])
		db.add_recipe(r)


###############################################################
#Index
#Reference: github.com/ctb/cse491-linkz
###############################################################
def generate_index_html():
	data = """
	<html>
	<head>
	<title>Index</title>
	<style type ="text/css">
		h1{color:red;}
	</style>
	<script>
	function myFunction()
	{
		alert("Hello! I am an alert box!");
	}
	</script>
	</head>
	<body>
	<h1>Drinkz </h1> 
<p> 
<a href='recipes.html'>Recipes</a>
</p>
<p>
<a href = 'inventory.html'>Inventory</a>
</p>
<p>
<a href = 'liquor_types.html'>Liquor Types</a>
</p>
<p>
<a href = 'convert_all_the_things_form'>Conversion Page</a>
</p>
<p>
	<input type="button" onclick="myFunction()" value="Show alert box" />
	</p>

</body>
</html>
	"""
	return data
###############################################################
#Recipes
#Reference: github.com/ctb/cse491-linkz
###############################################################
def generate_recipes_html():
	data = """
		<html>
	<head>
	<title>Recipes</title>
		<style type ="text/css">
		h1{color:red;}
	</style>
	</head>
	<body><h1> Recipes</h1>"""
	x = list(db.get_all_recipes())
	for recipe in x:
		data += "<h2>%s</h2>" % (recipe.getName())
		data += "<ul>"
		for ing in recipe.getIngredients():
			data += "<li>%s -- %s</li>" % (ing[0], ing[1])
		data += "</ul>"

	data += """<p> 
<a href='index.html'>Home</a>
</p>
<p>
<a href = 'inventory.html'>Inventory</a>
</p>
<p>
<a href = 'liquor_types.html'>Liquor Types</a>
</p>
<p>
<a href = 'convert_all_the_things_form'>Conversion Page</a>
</p>
</body>
</html>
"""
	return data

###############################################################
#Inventory
#Reference: github.com/ctb/cse491-linkz
###############################################################
def generate_inventory_html():
	data = """	<html>
	<head>
	<title>Inventory</title>
		<style type ="text/css">
		h1{color:red;}
	</style>
	</head>
	<body><h1> Inventory</h1>"""
	data += "<ul>"
	for bottle in db._inventory_db:
		data += "<li>%s -- %s -- %s ml</li>" % (bottle[0], bottle[1], db.get_liquor_amount(bottle[0], bottle[1]))
	data += "</ul>"

	data += """
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
<a href = 'convert_all_the_things_form'>Conversion Page</a>
</p>
</body>
</html>
"""
	return data

###############################################################
#Liquor Types
#Reference: github.com/ctb/cse491-linkz
###############################################################
def generate_liquor_types_html():
	data = """	<html>
	<head>
	<title>Liquor Types</title>
		<style type ="text/css">
		h1{color:red;}
	</style>
	</head>
	<body><h1> Types of Liquor Available for Your Pleasure</h1>"""
	data += "<ul>"
	for bottle in db._bottle_types_db:
		data += "<li>%s -- %s -- %s</li>" % (bottle[0], bottle[1], bottle[2])
	data += "</ul>"

	data += """
<p> 
<a href='index.html'>Home</a>
</p>
<p>
<a href = 'recipes.html'>Recipes</a>
</p>
<p>
<a href = 'inventory.html'>Inventory</a>
</p>
<p>
<a href = 'convert_all_the_things_form'>Conversion Page</a>
</p>
</body>
</html>
"""
	return data









