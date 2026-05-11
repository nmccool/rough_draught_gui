"""
Blueprint file for the Rough Draught Streamlit App.
"""

STYLE_OPTIONS = {
    1: "IPA",
    2: "Lager",
    3: "Pilsner",
    4: "Porter",
    5: "Stout",
    6: "Wheat",
    7: "Belgian / Farmhouse",
    8: "Sour",
    9: "Barleywine",
    10: "Other",
}


COUNTRY_OPTIONS = {
    1: "United States",
    2: "Germany",
    3: "Belgium",
    4: "United Kingdom",
    5: "Ireland",
    6: "Canada",
    7: "Mexico",
    8: "Other",
}


PACK_SIZE_OPTIONS = {
    1: "Single",
    2: "4-Pack",
    3: "6-Pack",
    4: "12-Pack",
    5: "24-Pack",
    6: "Draught Pour (Pint)",
    7: "Other",
}


CONTAINER_SIZE_OPTIONS = {
    1: "12 oz",
    2: "16 oz",
    3: "19.2 oz",
    4: "22 oz",
    5: "750 mL",
    6: "Other",
}


RATING_DESCRIPTIONS = {
    1: "Ugh. Should've Had a Zima 🤢",
    2: "Rough 😣",
    3: "Solid 👍🏻",
    4: "Pretty Damn Good 😎",
    5: "I Want to Brush My Teeth With It 😁",
}


class BeerEntry:
    """Beer tasting entry."""

    def __init__(
        self,
        timestamp,
        location,
        beer_name,
        brewery,
        beer_style,
        abv,
        strength,
        country,
        city,
        state,
        pack_size,
        container_size,
        price,
        buy_again,
        rating,
        rating_description,
        tasting_notes,
    ):
        self.timestamp = timestamp
        self.location = location
        self.beer_name = beer_name
        self.brewery = brewery
        self.beer_style = beer_style
        self.abv = abv
        self.strength = strength
        self.country = country
        self.city = city
        self.state = state
        self.pack_size = pack_size
        self.container_size = container_size
        self.price = price
        self.buy_again = buy_again
        self.rating = rating
        self.rating_description = rating_description
        self.tasting_notes = tasting_notes

    def to_dict(self):
        """Beer entry as a dictionary for CSV storage."""
        return {
            "timestamp": self.timestamp,
            "location": self.location,
            "beer_name": self.beer_name,
            "brewery": self.brewery,
            "beer_style": self.beer_style,
            "abv": self.abv,
            "strength": self.strength,
            "country": self.country,
            "city": self.city,
            "state": self.state,
            "pack_size": self.pack_size,
            "container_size": self.container_size,
            "price": self.price,
            "buy_again": self.buy_again,
            "rating": self.rating,
            "rating_description": self.rating_description,
            "tasting_notes": self.tasting_notes,
        }

    def summary(self):
        """Human readable summary of the beer entry."""
        return (
            f"{self.beer_name} by {self.brewery} | "
            f"{self.beer_style} | "
            f"{self.strength} | "
            f"Rating: {self.rating}/5"
        )


def determine_strength(abv):
    """Beer strength category based on ABV."""
    if abv == 0:
        return "ABV not provided"

    if abv < 4.9:
        return "Session"

    if abv <= 7.9:
        return "Standard"

    return "Imperial"


def validate_required_fields(beer_name, brewery):
    """Required beer entry field validation."""
    errors = []

    if not beer_name.strip():
        errors.append("Beer name is required.")

    if not brewery.strip():
        errors.append("Brewery is required.")

    return errors


def validate_style_choice(choice):
    """Beer style selection validation."""
    if choice not in STYLE_OPTIONS:
        return (
            "Invalid entry. Please select a valid number "
            "or select 10 (Other) to manually enter."
        )

    return None


def validate_country_choice(choice):
    """Country selection validation."""
    if choice not in COUNTRY_OPTIONS:
        return (
            "Invalid entry. Please select a valid number "
            "or select 8 (Other) to manually enter."
        )

    return None


def validate_pack_size_choice(choice):
    """Pack size selection validation."""
    if choice not in PACK_SIZE_OPTIONS:
        return (
            "Invalid entry. Please select a valid pack size number "
            "or select 7 (Other) to manually enter."
        )

    return None


def validate_container_size_choice(choice):
    """Container size selection validation."""
    if choice not in CONTAINER_SIZE_OPTIONS:
        return (
            "Invalid entry. Please select a valid container size number "
            "or select 6 (Other) to manually enter."
        )

    return None


def validate_abv(abv):
    """ABV range validation."""
    if abv < 0:
        return "ABV cannot be negative."

    if abv > 20:
        return (
            "Invalid ABV. Please enter a beer ABV "
            "between 0% and 20% or select 0 if unknown."
        )

    return None


def validate_price(price):
    """Price range validation."""
    if price < 0:
        return "Price cannot be negative."

    if price > 100:
        return "Invalid price. Please enter a price below $100."

    return None


def validate_other_field(value, field_name):
    """Manually entered field validation."""
    if not value.strip():
        return f"{field_name} is required when Other is selected."

    return None

def validate_us_location(city, state):
    """City and state validation when United States is selected."""
    errors = []

    if not city.strip():
        errors.append(
            "City is required for United States breweries."
        )

    if not state.strip():
        errors.append(
            "State is required for United States breweries."
        )

    return errors