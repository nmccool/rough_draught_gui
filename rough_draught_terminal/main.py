from rough_draught_terminal.beer_entry import BeerEntry

def main():
    beer1 = BeerEntry(
        "Corona",
        "Corona",
        12.99,
        4.5,
        "Pilsner",
        "Session",
        "Mexico",
        3
    )

    print("\n--- ORIGINAL ENTRY ---")
    beer1.display_entry()

    # --- Use setters ---
    beer1.set_price(11.99)
    beer1.set_rating(4)

    print("\n--- UPDATED ENTRY ---")
    beer1.display_entry()


main()