# Test functions in the macros.py file

import unittest
import sys
sys.path.append("..")
import macros

class TestMacroFunctions(unittest.TestCase):
    def test_CalculateMacros(self):
        """
        "Potato": Macros(Calories=77, Fat=0.09, Carbs=16.2, Fiber=2.2, Protein=2, Water=79, Sodium=6),
        "Beetroot": Macros(Calories=43, Fat=0.2, Carbs=6.8, Fiber=2.8, Protein=1.6, Water=87.6, Sodium=78),
        "Apple": Macros(Calories=52, Fat=0.2, Carbs=11.4, Fiber=2.4, Protein=0.3, Water=85.6, Sodium=1),
        """
        # Test that the correct macro values are obtained for 500 grams.
        potato = macros.Macros(Calories=385, Fat=0.45, Carbs=81, Fiber=11, Protein=10, Water=395, Sodium=30)
        beetroot = macros.Macros(Calories=215, Fat=1, Carbs=34, Fiber=14, Protein=8, Water=438, Sodium=390)
        apple = macros.Macros(Calories=260, Fat=1, Carbs=57, Fiber=12, Protein=1.5, Water=428, Sodium=5)

        self.assertEqual(potato, macros.CalculateMacros("Potato", 500))
        self.assertEqual(beetroot, macros.CalculateMacros("Beetroot", 500))
        self.assertEqual(apple, macros.CalculateMacros("Apple", 500))

unittest.main()
