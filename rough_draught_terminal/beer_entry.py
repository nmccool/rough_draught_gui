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

# --- Setters ---
    def set_beer_name(self, beer_name):
        self.__beer_name = beer_name

    def set_brewery(self, brewery):
        self.__brewery = brewery

    def set_price(self, price):
        self.__price = price

    def set_abv(self, abv):
        self.__abv = abv

    def set_style(self, style):
        self.__style = style

    def set_strength(self, strength):
        self.__strength = strength

    def set_country(self, country):
        self.__country = country

    def set_rating(self, rating):
        self.__rating = rating

# --- Display ---
    def display_entry(self):
        print("1. Beer Name:", self.__beer_name)
        print("2. Brewery:", self.__brewery)
        print(f"3. Price: ${self.__price:.2f}")
        print(f"4. ABV: {self.__abv:.1f}%")
        print("5. Style:", self.__style)
        print("6. Strength:", self.__strength)
        print("7. Country:", self.__country)
        print("8. Rating:", self.__rating)