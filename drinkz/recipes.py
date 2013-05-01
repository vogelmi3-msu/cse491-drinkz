import db
#import the database so we can use it..
class Recipe:
    def __init__(self, name = '', ingredients = []):
        self.name = name
        self.ingredients = ingredients

    def getName(self):
    	return self.name

    def getIngredients(self):
    	return self.ingredients

    def need_ingredients(self):
		needed = []
		#loop through ingredients
		for (typ, needed_amount) in self.ingredients:
			needed_amount = db.convert_to_ml(needed_amount)
			#check supply
			supply = db.check_inventory_for_type(typ)
			if supply:
				total_amount = 0
				for m,l in supply:
					total_amount = db.get_liquor_amount(m,l)
				if needed_amount - total_amount > 0:
					#we don't have enough :(
					needed_amount = needed_amount - total_amount
				else:
					continue
			
			needed.append((typ, needed_amount))

		if needed == []:
			return False
		else:

			return needed
