-- Create the macro tracker database tables

-- "Calories Fat Carbs Fiber Protein Water Sodium Date"
CREATE TABLE Macros (
	ID integer primary key autoincrement, -- This is irrelevant for us.
	Calories real,
	Fat real,
	Carbs real,
	Fiber real,
	Protein real,
	Water real,
	Sodium real,
	Date text -- String of D/M/Y: '11/8/2019' for 11th of August 2019.
);

-- Now user settings
-- This table stores the user's macro target settings,
-- such as calorie limit, protein target, etc
-- It only contains one row which gets updated when the user changes the settings.
-- I chose this instead of a config file for the sake of completeness when it comes to usage.
CREATE TABLE Settings (
	ID integer primary key autoincrement, -- Once again, irrelevant for us.
	Calories real,
	Fat real,
	Carbs real,
	Fiber real,
	Protein real,
	Water real,
	Sodium real
);

-- Now individual food item logs.
-- Each row stores the food item's name, its weight, and the date.
-- This is simply to allow the user to track which foods they've eaten on a given date.
CREATE TABLE Foods (
	ID integer primary key autoincrement,
	Name text, -- 'Potato',
	Weight real, -- in grams
	Date text -- Same as in the Macros table
);
