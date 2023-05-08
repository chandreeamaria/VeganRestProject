# This program is an implementation of a menu app for a manager of a Vegan Restaurant

# Class engine in module inflect.py provide plural inflections
# Importing Ingredient and Recipe classes from ingredient.py

import csv
import sys
import inflect
import os
from ingredient import Ingredient, Recipe
from tabulate import tabulate

def main():
    create_options()
    option = int(input("Insert choice: "))
    try:
        match option:
            case 1:
                add_recipe("products.csv","recipes.csv")
            case 2:
                delete_recipe("recipes.csv", input("Enter recipe's name that needs to be deleted: "))
            case 3:
                view_products("products.csv")
            case 4:
                add_new_product("products.csv")
            case 5:
                delete_product("products.csv", input("Enter product's name that needs to be deleted: "))
            case 6:
                print(show_recipe_calories("recipes.csv", input("Introduce recipe's name: ")))
            case 7:
                print(show_recipe_price("recipes.csv", input("Introduce recipe's name: ")))
            case 8:
                print(view_menu("recipes.csv"))
            case 0:
                sys.exit()
            case _:
                print("Invalid choice. Please run again and choose a number from above.")
    except FileNotFoundError:
        sys.exit("File does not exist")


def create_options():
    # Defines a dictionary with the options for manager/employee to insert.

    options = {
        1 : "Add recipe",
        2 : "Delete recipe",
        3 : "View available products",
        4 : "Add new product",
        5 : "Delete product",
        6 : "Show some recipe's calories",
        7 : "Show some recipe's price",
        8 : "View menu",
        0 : "Exit"
    }
    for k in options:
        print(k, "--", options[k])

def _is_empty_file(path):
    # Checks if csv file is empty.

    return os.stat(path).st_size == 0

def add_recipe(products_path, recipes_path):

    # Adds a recipe to the menu
    # Prompts the user for recipe's name firstly
    # Prompts the user for ingredients in the recipe with the respective quantities until the user inputs control-d
    # Raises ValueError if ingredient is not from the available products csv file
    # After user inputs control-d, program prompts the user for the price too
    # Recipes are written in a separate csv file


    print("!!!When you finish introducing ingredients please use CTRL+D then add also the price for the recipe!!!")
    print("!!!To check if recipe is added, open the menu again and use option 8!!!")
    recipe_name = input("Enter recipe's name: ")
    recipe_get = get_recipes(recipes_path)
    for recipe in recipe_get:
        if recipe_name == recipe.name:
            sys.exit("Recipe already in the menu")
    total_calories = 0
    ingredients = []
    recipes=[]
    while True:
        try:
            found = False
            name_ingredient = input("Enter ingredient's name: ").lower().strip()
            quantity = float(input("Enter quantity: "))
            for product in get_products(products_path):
                if name_ingredient == product.name:
                    found = True
                    ingredients.append(name_ingredient)
                    total_calories += quantity * int(product.calories)
                    print(total_calories)
            if found == False:
                raise ValueError
        except ValueError:
            print("!!!Not from list of products!!!")
            pass
        except EOFError:
            print()
            price = input("Enter recipe's price: ").lower().strip()
            p = inflect.engine()
            ingredients = p.join((ingredients))
            recipes.append(Recipe(recipe_name,ingredients,total_calories,price))
            with open(recipes_path, "a") as file:
                writer = csv.DictWriter(file, fieldnames=["recipes", "ingredients","calories","price"])
                if _is_empty_file(recipes_path):
                    writer.writeheader()
                for recipe in recipes:
                    writer.writerow({"recipes" : recipe.name, "ingredients" : recipe.ingredients, "calories" : recipe.calories, "price" : f"{recipe.price} lei"})
            break

def get_recipes(path):

    # Reads csv file for recipes
    # Returns a list of Recipe objects

    recipes = []
    with open(path) as file:
        reader = csv.DictReader(file)
        for row in reader:
            recipes.append(Recipe(row["recipes"],row["ingredients"],row["calories"],row["price"]))
        return recipes

def delete_recipe(path, delete_recipe):

    # Deletes a recipe from menu
    # Raises ValueError if recipe cannot be found in the menu
    # Rewrites csv file for recipes with recipes that were not removed

    recipes = get_recipes(path)
    flag = 0
    for recipe in recipes:
        if delete_recipe == recipe.name:
            flag = 1
            recipes.remove(recipe)
    if flag == 0:
        raise ValueError("Not on the menu")
    with open(path, "w") as file:
         writer = csv.DictWriter(file, fieldnames=["recipes", "ingredients", "calories","price"])
         if _is_empty_file(path):
             writer.writeheader()
         for recipe in recipes:
             writer.writerow({"recipes" : recipe.name, "ingredients" : recipe.ingredients, "calories" : recipe.calories, "price" : recipe.price})

def view_products(path):

    # Displays name and calories attributes from class Ingredient sorted alphabetically

    for product in sorted(get_products(path), key=lambda product : product.name):
        print(product.name, product.calories)

def get_products(path):

    # Reads csv file for available products in the cafe
    # Returns a list of Ingredient objects

    products = []
    with open(path) as file:
        reader = csv.DictReader(file)
        for row in reader:
            products.append(Ingredient(row["products"],row["calories"]))
        return products

def add_new_product(path):

    # Adds a new product
    # Prompts the user for new product name and product calories
    # Raises ValueError if product is already in the list
    # Rewrites csv file with the new product added

    new_product = input("Enter new product name: ")
    flag=0
    for product in get_products(path):
        if new_product == product.name:
            flag = 1
            raise ValueError("Product is already in the list")
    if flag == 0:
        new_calories = input("Enter new product calories: ")
        with open(path, "a") as file:
            writer = csv.DictWriter(file, fieldnames=["products", "calories"])
            writer.writerow({"products" : new_product, "calories" : new_calories})

def delete_product(path, delete_product):

    # Deletes a product from the list of available products
    # Rewrites csv file for available products with products that were not removed

    products = get_products(path)
    for product in products:
        if delete_product == product.name:
            products.remove(product)
    with open(path, "w") as file:
         writer = csv.DictWriter(file, fieldnames=["products", "calories"])
         if _is_empty_file(path):
             writer.writeheader()
         for product in products:
             writer.writerow({"products" : product.name, "calories" : product.calories})

def show_recipe_calories(path, rec):

    # Prompts the user for a recipe name
    # Returns the number of calories for the input recipe
    # Raises ValueError if recipe is not on the menu

    recipes = get_recipes(path)
    flag = 0
    for recipe in recipes:
        if rec == recipe.name:
            flag = 1
            return f"{float(recipe.calories):.0f} calories"
    if flag == 0:
        raise ValueError("Not on the menu")

def show_recipe_price(path, rec):

    # Prompts the user for a recipe name
    # Returns the price for the input recipe
    # Raises ValueError if recipe is not on the menu

    recipes = get_recipes(path)
    flag = 0
    for recipe in recipes:
        if rec == recipe.name:
            flag =1
            return f"{recipe.price}"
    if flag == 0:
        raise ValueError("Not on the menu")

def view_menu(path):

    # Displays the cafe menu as a table using tabulate with github format

    table=[]
    headers=[]
    with open(path) as file:
        reader = csv.DictReader(file)
        for row in reader:
            headers = list(row.keys())
            table.append([row[headers[0]],row[headers[1]],row[headers[2]],row[headers[3]]])
        return tabulate(table, headers, tablefmt="github")

if __name__ == "__main__":
    main()
