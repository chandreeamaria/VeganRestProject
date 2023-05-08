class Ingredient:
    def __init__(self,name,calories):
        if not name:
            raise ValueError("Invalid name")
        if not calories:
            raise ValueError("Please add calories")
        self.name = name
        self.calories = calories
    def __str__(self):
        return f"{self.name} has {self.calories} calories"

    @property
    def calories(self):
        return self._calories
    @calories.setter
    def calories(self,calories):
        self._calories = calories

class Recipe:
    def __init__(self,name,ingredients,calories,price):
        if not name:
            raise ValueError("Invalid name")
        if not calories:
            raise ValueError("Please add calories")
        self.name = name
        self.ingredients = ingredients
        self.calories = calories
        self.price = price
    def __str__(self):
        return f"{self.name} {self.ingredients} {float(self.calories):.0f} calories {float(self.price):.0f} lei"

    @property
    def calories(self):
        return self._calories
    @calories.setter
    def calories(self,calories):
        self._calories = calories

    @property
    def price(self):
        return self._price
    @price.setter
    def price(self,price):
        self._price = price
