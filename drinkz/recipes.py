
class Recipe:
    def __init__(self, name = '', ingredients = []):
        self.name = name
        self.ingredients = ingredients

    def getname(self):
    	return self.name

    def getIngredients(self):
    	return self.ingredients


