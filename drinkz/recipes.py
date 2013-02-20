"""
A file containing everything except a recipe for disaster
"""

import db

class Recipe(object):
	def __init__(self, name, ingredients):
		self.name = name
		self.ingredients = ingredients
	
	def __str__(self):
		'''override for getting string value of recipe'''
		recipe_str = self.name + ': '
		for ingred in self.ingredients:
			recipe_str += ' ' + ingred[0] + '- ' + ingred[1]
		return recipe_str
	
	def get_html_str(self):
		'''returns html representation of recipe'''
		recipe_str = '<b>' + self.name + '</b>: '
		for ingred in self.ingredients:
			recipe_str += ' ' + ingred[0] + '- <i>' + ingred[1] + '</i>'
		
		if self.need_ingredients():
			recipe_str +=  '\t\t<b>YES</b>' 
		else:
			recipe_str +=  '\t\t<b>NO</b>' 
		
		return recipe_str
	
	def need_ingredients(self):
		needed = []
		
		#loop through ingredients
		for (typ, needed_amount) in self.ingredients:
			needed_amount = db.convert_to_ml(needed_amount)
			
			#check supply
			supply = db.check_inventory_for_type(typ)
			if supply:
				tot_amount = 0
				for m,l in supply:
					if tot_amount <  db.get_liquor_amount(m,l):
						tot_amount = db.get_liquor_amount(m,l)
				
				if needed_amount - tot_amount > 0:
					#we don't have enough :(
					needed_amount = needed_amount - tot_amount
				else:
					# we've got enough! YUS
					continue
			
			needed.append((typ, needed_amount))
		
		return needed
			