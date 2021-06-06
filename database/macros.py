from collections import namedtuple

Macros = namedtuple("Macros", ("calories", "fat", "carbs", "fiber", "protein", "water", "sodium"))

units = {
        "calories": "kcal",
        "fat": "g",
        "carbs": "g",
        "fiber": "g",
        "protein": "g",
        "water": "g",
        "sodium": "mg",
    }

food_data = {
    # Raw fruits and vegetables
    'Potato': Macros(calories=77, fat=0.09, carbs=17, fiber=2.2, protein=2, water=79, sodium=6), 
    'Beetroot': Macros(calories=43, fat=0.2, carbs=6.8, fiber=2.8, protein=1.6, water=87.6, sodium=78), 
    'Apple': Macros(calories=52, fat=0.2, carbs=11.4, fiber=2.4, protein=0.3, water=85.6, sodium=1), 
    'Tomato': Macros(calories=18, fat=0.2, carbs=2.7, fiber=1.2, protein=0.9, water=94.5, sodium=5), 
    'Onion': Macros(calories=40, fat=0.1, carbs=7.6, fiber=1.7, protein=1.1, water=89.1, sodium=4), 
    'Garlic': Macros(calories=149, fat=0.5, carbs=31, fiber=2.1, protein=6.4, water=58.6, sodium=17), 
    'Zucchini': Macros(calories=16, fat=0.2, carbs=2.2, fiber=1.1, protein=1.2, water=94.6, sodium=10), 
    'Eggplant': Macros(calories=24, fat=0.2, carbs=2.3, fiber=3.4, protein=1, water=92.4, sodium=2), 
    'Cabbage': Macros(calories=25, fat=0.1, carbs=3.3, fiber=2.5, protein=1.3, water=92.2, sodium=18), 
    'Red cabbage': Macros(calories=31, fat=0.2, carbs=5.3, fiber=2.1, protein=1.4, water=90.4, sodium=27), 
    'Cauliflower': Macros(calories=25, fat=0.1, carbs=2.8, fiber=2.5, protein=2, water=91.9, sodium=30), 
    'Red bellpepper': Macros(calories=31, fat=0.3, carbs=4.2, fiber=2.1, protein=1, water=92.2, sodium=4), 
    'Banana': Macros(calories=89, fat=0.3, carbs=20.2, fiber=2.6, protein=1.1, water=74.9, sodium=1), 
    'Galia melon': Macros(calories=23, fat=0.2, carbs=3.78, fiber=1.8, protein=0.62, water=0, sodium=64), 
    'Butternut squash': Macros(calories=45, fat=0.1, carbs=9.7, fiber=2, protein=1, water=86.4, sodium=4), 
    'Carrot': Macros(calories=41, fat=0.24, carbs=6.8, fiber=2.8, protein=0.93, water=88, sodium=69), 
    'Cucumber': Macros(calories=16, fat=0.11, carbs=3.13, fiber=0.5, protein=0.65, water=95, sodium=2), 
    'Broccoli': Macros(calories=34, fat=0.4, carbs=4, fiber=2.6, protein=2.8, water=89.3, sodium=33), 
    'Leek': Macros(calories=61, fat=0.3, carbs=12.4, fiber=1.8, protein=1.5, water=83, sodium=20), 
    'Orange': Macros(calories=47, fat=0.12, carbs=9.35, fiber=2.4, protein=0.94, water=86.7, sodium=0), 
    'Sweet potato': Macros(calories=86, fat=0.05, carbs=20, fiber=3, protein=1.6, water=77, sodium=55), 
    'Pumpkin': Macros(calories=26, fat=0.1, carbs=6, fiber=0.5, protein=1, water=91.6, sodium=1), 
    'Date': Macros(calories=267, fat=0, carbs=61, fiber=8.6, protein=1.4, water=0, sodium=0), 
    'Baresa olives': Macros(calories=155, fat=16, carbs=0.5, fiber=3.3, protein=1, water=75.3, sodium=3380), 
    'Cosmopolitan lettuce': Macros(calories=15, fat=0.3, carbs=1.5, fiber=1, protein=1, water=94.6, sodium=8), 
    'Celery': Macros(calories=16, fat=0.2, carbs=1.8, fiber=1.6, protein=0.7, water=95.4, sodium=80), 
    # Dry beans, lentils, grains, flours
    'Brown beans': Macros(calories=320, fat=1.5, carbs=45, fiber=16, protein=22, water=0, sodium=100), 
    'Red lentils': Macros(calories=350, fat=1.3, carbs=50, fiber=12, protein=24, water=0, sodium=100), 
    'Green lentils': Macros(calories=330, fat=1, carbs=49, fiber=12, protein=24, water=0, sodium=100), 
    'Chickpeas': Macros(calories=350, fat=4.8, carbs=50, fiber=10, protein=21, water=0, sodium=70), 
    'Whole wheat flour': Macros(calories=330, fat=3, carbs=56, fiber=13, protein=14, water=0, sodium=5), 
    'White flour': Macros(calories=349, fat=1.4, carbs=71.5, fiber=2.4, protein=11.4, water=0, sodium=10), 
    'Rye flour': Macros(calories=320, fat=2, carbs=59, fiber=20, protein=10, water=0, sodium=0), 
    'Quinoa': Macros(calories=380, fat=6.1, carbs=64, fiber=7, protein=14, water=0, sodium=10), 
    'Barley groats': Macros(calories=340, fat=2, carbs=66, fiber=11, protein=8, water=0, sodium=5), 
    'Barley flakes': Macros(calories=350, fat=2, carbs=66, fiber=11, protein=10, water=0, sodium=0), 
    'Rye flakes': Macros(calories=332, fat=2, carbs=60, fiber=17, protein=10, water=0, sodium=2), 
    'Oat flakes': Macros(calories=364, fat=7.5, carbs=54, fiber=11, protein=14, water=0, sodium=0), 
    # Misc.
    'Marmite': Macros(calories=260, fat=0.5, carbs=30, fiber=1.1, protein=34, water=0, sodium=10800), 
    'Bio tofu': Macros(calories=107, fat=5.3, carbs=0.2, fiber=0, protein=13.1, water=0, sodium=50), 
    'SoFine tofu': Macros(calories=128, fat=7.6, carbs=1, fiber=0.9, protein=13.4, water=0, sodium=30), 
    'Pirkka corn': Macros(calories=76, fat=1, carbs=14, fiber=2.2, protein=2.3, water=0, sodium=650), 
    'Whole-wheat couscous': Macros(calories=338, fat=1.5, carbs=65, fiber=8, protein=12, water=0, sodium=40), 
    'Freshona frozen corn': Macros(calories=97, fat=1.8, carbs=16, fiber=2.7, protein=3.4, water=75.96, sodium=0), 
    'Freshona froze green beans': Macros(calories=32, fat=0.1, carbs=3.8, fiber=2.7, protein=1.9, water=90.3, sodium=30), 
    'Pirkka kidney beans': Macros(calories=77, fat=0.6, carbs=6.8, fiber=5.7, protein=8.1, water=0, sodium=300), 
    'Salt': Macros(calories=0, fat=0, carbs=0, fiber=0, protein=0, water=0, sodium=38758), 
    'White sugar': Macros(calories=400, fat=0, carbs=100, fiber=0, protein=0, water=0, sodium=0), 
}

# Food IDs dictionary, populated
# based on the keys in the food data dictionary.
# This dictionary is simply used to make the command line usage easier
# by allowing users to use the food's ID rather than its name, 
# if the name is long and cumbersome to type
foodIds = {}
for i, key in enumerate(food_data):
    foodIds[i] = key

def CalculateMacros(food, weight):
    # Calculate the macros and return a namedtuple with the results
    # Example call: values = calculateMacros("Potato")
    # Will raise KeyError if the food doesn't exist
    
    if weight <= 0:
        raise ValueError("weight must be above 0")
    macroValues = food_data[food]._asdict()
    multiply = weight / 100
    
    # Now multiply each value by the weight and round it to 3 decimal points.
    for key in macroValues:
        value = macroValues[key]
        macroValues[key] = round(value * multiply, 3)
    
    # Return the namedtuple constructed from the dictionary
    # NOTE: might have to return a dictionary here for JSON
    return Macros(**macroValues)
