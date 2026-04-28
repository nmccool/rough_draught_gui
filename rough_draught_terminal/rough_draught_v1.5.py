"""
-----------------------------------------------------------------------
ASSIGNMENT 14A: Object practice
-----------------------------------------------------------------------
[X] 1. Header Docstring included.
[ ] 2. Define a class for a part of your project using PascalCase.
[ ] 3. Use __init__ to set private attributes (__variable).
[ ] 4. Write Setters and Getters for the attributes.
[ ] 5. Write a summary function that returns a formatted description.
[ ] 6. Instantiate two distinct objects and print their summaries.
-----------------------------------------------------------------------
Name: Neal McCool
Date: 2026-04-20
"""

# --- Welcome to Rough Draught---
# The purpose of this project is to enable users to keep track
# of the good beers as well as the 'rough draughts' they've had
# over time.  As their log grows they will ensure that they only
# repurchase the good ones and don't accidentally buy bad ones again.

# Eventually this project format could be reworked for a
# variety of other products like wine, or even coffee.


import datetime

class BeerEntry:
    def __init__(self, beer_name, brewery, price, abv, style, strength, country, rating):
        self.__beer_name = beer_name
        self.__brewery = brewery
        self.__price = price
        self.__abv = abv
        self.__style = style
        self.__strength = strength
        self.__country = country
        self.__rating = rating

# --- Getters ---
    def get_beer_name(self):
        return self.__beer_name

    def get_brewery(self):
        return self.__brewery

    def get_price(self):
        return self.__price

    def get_abv(self):
        return self.__abv

    def get_style(self):
        return self.__style

    def get_strength(self):
        return self.__strength

    def get_country(self):
        return self.__country

    def get_rating(self):
        return self.__rating

# --- Summary ---
    def get_summary(self):
        return (f"{self.__beer_name} | {self.__brewery} | "
                f"${self.__price:.2f} | {self.__abv:.1f}% | "
                f"{self.__style} | {self.__rating}")

# --- GLOBAL CONSTANTS (Brewery Rules) ---
BEER_FILE = "beer_file.txt"
DATA_FILE = "entry_history.txt"
HUMAN_REPORT = "human_report.txt"

# TODO replace location with 'where purchased' it's more relevant than city/state.

#  --- Asks for user's name and location ---
def get_user_info():
    name = input("Enter your name: ").strip().title()
    location = input("Enter your City, State: ").strip().title()
    return name, location

# --- Reads beer identifiers from external file into a dictionary ---
def load_beer_file():
    beer_dictionary = {}

    try:
        with open(BEER_FILE, "r") as file:
            for line in file:
                line = line.strip()
                category, items = line.split(":")
                beer_dictionary[category] = [item.strip() for item in items.split(",")]
    except FileNotFoundError:
        print("Error! beer_file.txt missing!")

    return beer_dictionary

# --- Collects beer entry data ---
def collect_beer_data(beer_dictionary, rating=0):
    styles = beer_dictionary["Styles"]
    strengths = beer_dictionary["Strengths"]
    countries = beer_dictionary["Countries"]
    
# --- Name of beer ---
    beer_name = input("Beer Name: ").strip().title()

# --- Name of brewery ---
    brewery = input("Brewery: ").strip().title()

# TODO add option to select "single, 4pk, 6pk, 12pk etc.".  Price is moot if we don't know how many were purchased. 

# --- Price paid ---
    price = float(input("Price: $"))

# TODO add 'unknown' option as some beers do not indicate abv on the label.

# --- Alcohol amount ---
    abv = float(input("ABV (%): "))

# TODO if user selects "other" there's no code for them to input their answer. 

# --- Style ---
    print("\nSelect a Style:")
    for index, style in enumerate(styles, start=1):
        print(f"{index}. {style}")
    style_choice = int(input("Enter style number: "))
    style = styles[style_choice - 1]

# --- Strength ---
    print("\nSelect a Strength:")
    for index, strength in enumerate(strengths, start=1):
        print(f"{index}. {strength}")
    strength_choice = int(input("Enter strength number: "))
    strength = strengths[strength_choice - 1]

# TODO if user selects "other" there's no code for them to input their answer.
# TODO replace country with region or state.  Most craft beers available in IL are domestic, which makes 'Country' not as necessary.

# --- Country ---
    print("\nSelect a Country:")
    for index, country in enumerate(countries, start=1):
        print(f"{index}. {country}")
    country_choice = int(input("Enter country number: "))
    country = countries[country_choice - 1]

# TODO add "Tasting Notes" section

# --- Rating ---
    while True:
        user_rating = input("Rate beer 1-5 or press 'ENTER' to skip: ").strip()
        if user_rating == "":
            break
        elif user_rating.isdigit() and 1 <= int(user_rating) <= 5:
            rating = int(user_rating)
            break
        else:
            print("Invalid selection. Please enter a rating 1-5.")


    return BeerEntry(
    beer_name,
    brewery,
    price,
    abv,
    style,
    strength,
    country,
    rating
    )

# --- Calculated Rating ---
def calculate_rating(beer_entry):
    return beer_entry.get_rating()

# --- Saving data ---
def save_data_and_label(name, location, beer_entry, rating_result):
    print("-" * 50)
    print("ROUGH DRAUGHT ENTRY")
    print("-" * 50)
    print(f"User: {name}")
    print(f"Location: {location}")
    print(f"Beer: {beer_entry.get_beer_name()}")
    print(f"Brewery: {beer_entry.get_brewery()}")
    print(f"Price: ${beer_entry.get_price():.2f}")
    print(f"ABV: {beer_entry.get_abv():.1f}%")
    print(f"Rating: {rating_result}")
    print("-" * 50)

    current_time = datetime.datetime.now()
    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S")

# --- Raw Data File (Append) ---
    with open(DATA_FILE, "a") as file:
        file.write(
            f"{timestamp} | "
            f"{name} | "
            f"{location} | "
            f"{beer_entry.get_beer_name()} | "
            f"{beer_entry.get_brewery()} | "
            f"{beer_entry.get_price():.2f} | "
            f"{beer_entry.get_abv():.1f} | "
            f"{beer_entry.get_style()} | "
            f"{beer_entry.get_strength()} | "
            f"{beer_entry.get_country()} | "
            f"{rating_result}\n"
        )
# TODO add code to display rating in Human Report as star emoji instead of number
# --- Human Report File (Write) ---
    with open(HUMAN_REPORT, "w") as file:
        file.write("-" * 50 + "\n")
        file.write("ROUGH DRAUGHT ENTRY\n")
        file.write("-" * 50 + "\n")
        file.write(f"Timestamp: {timestamp}\n")
        file.write(f"User: {name}\n")
        file.write(f"Location: {location}\n")
        file.write(f"Beer: {beer_entry.get_beer_name()}\n")
        file.write(f"Brewery: {beer_entry.get_brewery()}\n")
        file.write(f"Price: ${beer_entry.get_price():.2f}\n")
        file.write(f"ABV: {beer_entry.get_abv():.1f}%\n")
        file.write(f"Style: {beer_entry.get_style()}\n")
        file.write(f"Strength: {beer_entry.get_strength()}\n")
        file.write(f"Country: {beer_entry.get_country()}\n")
        file.write(f"Rating: {rating_result}\n")

    print(f"Success! Your entry is saved." + "\n")

# --- Review stored entries ---
def review_entry_history():
    try:
        with open(DATA_FILE, "r") as file:
            print("-" * 50)
            print("ENTRY HISTORY REVIEW")
            print("-" * 50)
            for line in file:
                print(line.strip())
    except FileNotFoundError:
        print("Error: entry history file not found.")

def main():
# --- Load external beer info ---
    beer_dictionary = load_beer_file()

    if not beer_dictionary:
        return

# --- Get User Info ---
    name, location = get_user_info()

# --- Data Collection ---
    beer_entry = collect_beer_data(beer_dictionary)

# --- Rating Calculation ---
    rating_result = calculate_rating(beer_entry)

# --- Handoff ---
    save_data_and_label(
        name=name,
        location=location,
        beer_entry=beer_entry,
        rating_result=rating_result
    )

# --- Review Entry ---
    review_entry_history()

main()

print("\n" + "-" * 50)
print("CLASS OBJECT SUMMARY TEST")
print("-" * 50)
beer1 = BeerEntry("Corona", "Corona", 12.99, 4.5, "Pilsner", "Session", "Mexico", 3)
beer2 = BeerEntry("Pliny The Elder", "Russian River", 9.99, 8.0, "IPA", "Imperial", "USA", 5)

print(beer1.get_summary())
print(beer2.get_summary())