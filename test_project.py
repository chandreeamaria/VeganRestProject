from project import show_recipe_calories, show_recipe_price, delete_recipe
import pytest

"""
some data was already added in products.csv and recipes.csv so that testing can be possible:
"""

def test_recipe_exists():
    with pytest.raises(ValueError):
        show_recipe_calories("recipes.csv","salado")
    with pytest.raises(ValueError):
        show_recipe_price("recipes.csv","limo")
    with pytest.raises(ValueError):
        delete_recipe("recipes.csv","limo")
def test_show_recipe_calories():
    assert show_recipe_calories("recipes.csv","Broccoli salad") == "360 calories"
    assert show_recipe_calories("recipes.csv","Vegan rice pilaf") == "522 calories"
def test_show_recipe_price():
    assert show_recipe_price("recipes.csv","Broccoli salad") == "35 lei"
    assert show_recipe_price("recipes.csv","Vegan rice pilaf") == "40 lei"
