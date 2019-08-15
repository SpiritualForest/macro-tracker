# Macro tracker macros file.
# This file contains dictionaries of macro values,
# in grams per 100g of each food

# NOTE: 
# Do not modify the values unless you are absolutely sure.
# Otherwise, you might get incorrect results.
# Of course, if you do modify the values and get wrong results, that's your problem :-)
from collections import namedtuple

# All macro values are in grams, except sodium which is in milligrams (mg)
Macros = namedtuple("Macros", "Calories Fat Carbs Fiber Protein Water Sodium")

# Strings for displaying data after retrieval from the database
units = {
        "Calories": "kcal",
        "Fat": "g",
        "Carbs": "g",
        "Fiber": "g",
        "Protein": "g",
        "Water": "g",
        "Sodium": "mg",
    }

# Food data
# TODO: Do not hard code values here! Read from a file that users can extend using the UI in some way.
# Load it up into a dictionary here at runtime.
data = {
        # Raw vegetables first
        "Potato": Macros(Calories=77, Fat=0.09, Carbs=16.2, Fiber=2.2, Protein=2, Water=79, Sodium=6),
        "Beetroot": Macros(Calories=43, Fat=0.2, Carbs=6.8, Fiber=2.8, Protein=1.6, Water=87.6, Sodium=78),
        "Apple": Macros(Calories=52, Fat=0.2, Carbs=11.4, Fiber=2.4, Protein=0.3, Water=85.6, Sodium=1),
        "Tomato": Macros(Calories=18, Fat=0.2, Carbs=2.7, Fiber=1.2, Protein=0.9, Water=94.5, Sodium=5),
        "Onion": Macros(Calories=40, Fat=0.1, Carbs=7.6, Fiber=1.7, Protein=1.1, Water=89.1, Sodium=4),
        # Beans, lentils, etc
        # NOTE: macros for dry, not cooked.
        "Brown beans": Macros(Calories=320, Fat=1.5, Carbs=45, Fiber=16, Protein=22, Water=0, Sodium=100),
        "Red lentils": Macros(Calories=350, Fat=1.3, Carbs=50, Fiber=12, Protein=24, Water=0, Sodium=100),
        "Chickpeas": Macros(Calories=350, Fat=4.8, Carbs=50, Fiber=10, Protein=21, Water=0, Sodium=70),
        "Whole wheat flour": Macros(Calories=330, Fat=3, Carbs=56, Fiber=13, Protein=14, Water=0, Sodium=5),
        "Belbake rye flour": Macros(Calories=318, Fat=1.7, Carbs=59.7, Fiber=14, Protein=9, Water=0, Sodium=10),
        # Processed
        "Barley groats": Macros(Calories=340, Fat=2, Carbs=66, Fiber=11, Protein=8, Water=0, Sodium=5),
        "Rye flakes": Macros(Calories=332, Fat=2, Carbs=60, Fiber=17, Protein=10, Water=0, Sodium=2),
        "K-Menu canned white mushrooms": Macros(Calories=18, Fat=0.2, Carbs=0.9, Fiber=2.2, Protein=2.1, Water=170, Sodium=600),
        "Marmite": Macros(Calories=260, Fat=0.5, Carbs=30, Fiber=1.1, Protein=34, Water=0, Sodium=10800),
        "K-Menu crushed tomatoes": Macros(Calories=27, Fat=0.2, Carbs=4, Fiber=1.5, Protein=1.2, Water=94.5, Sodium=0),
    }

# Food IDs dictionary, populated
# based on the keys in the food data dictionary.
# This dictionary is simply used to make the command line usage easier
# by allowing users to use the food's ID rather than its name, 
# if the name is long and cumbersome to type
foodIds = {}
for i, key in enumerate(data):
    foodIds[i] = key

def CalculateMacros(food, weight):
    # Calculate the macros and return a namedtuple with the results
    # Example call: values = calculateMacros("Potato")
    # Returns None in case of an error.
    if food not in data:
        # No such food
        print("Error. Food item not found: {}".format(food))
        return
    if weight < 0:
        # Negative weight? LOLWUT, no.
        print("Error. Sub-zero weight provided.")
        return
    
    macroValues = data[food]._asdict()
    multiply = weight / 100
    
    # Now multiply each value by the weight and round it to 3 decimal points.
    for key in macroValues:
        value = macroValues[key]
        macroValues[key] = round(value * multiply, 3)
    
    # Return the namedtuple constructed from the dictionary
    return Macros(**macroValues)