"""
Rough Draught Streamlit App
MVP v2: Create, save, view, and search beer tasting entries.
"""

from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st
import base64

from blueprints import (
    BeerEntry,
    determine_strength,
    validate_required_fields,
    validate_style_choice,
    validate_country_choice,
    validate_pack_size_choice,
    validate_container_size_choice,
    validate_abv,
    validate_price,
    validate_other_field,
    validate_us_location,
    STYLE_OPTIONS,
    COUNTRY_OPTIONS,
    PACK_SIZE_OPTIONS,
    CONTAINER_SIZE_OPTIONS,
    RATING_DESCRIPTIONS,
)


BASE_DIR = Path(__file__).parent

ASSETS_DIR = BASE_DIR / "assets"
DATA_DIR = BASE_DIR / "data"

LOGO_FILE = ASSETS_DIR / "RoughDraughtLogoT.png"
BACKGROUND_FILE = ASSETS_DIR / "Notepad.png"

DATA_FILE = DATA_DIR / "beer_entries.csv"

CENTRAL_TIME = ZoneInfo("America/Chicago")


def ensure_data_file():
    """Create the data folder and CSV file if they do not exist."""
    DATA_DIR.mkdir(exist_ok=True)

    if not DATA_FILE.exists():
        df = pd.DataFrame(
            columns=[
                "timestamp",
                "location",
                "beer_name",
                "brewery",
                "beer_style",
                "abv",
                "strength",
                "country",
                "city",
                "state",
                "pack_size",
                "container_size",
                "price",
                "buy_again",
                "rating",
                "rating_description",
                "tasting_notes",
            ]
        )
        df.to_csv(DATA_FILE, index=False)


def load_entries():
    """Load beer entries from the CSV file."""
    ensure_data_file()
    return pd.read_csv(DATA_FILE)


def save_entry(entry):
    """Save a new beer entry to the CSV file."""
    df = load_entries()
    new_entry = pd.DataFrame([entry.to_dict()])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)


def get_base64_image(image_path):
    """Convert an image file to base64 for CSS use."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def load_custom_css():
    """Add some style to the app (this is my wheelhouse)"""
    if BACKGROUND_FILE.exists():
        background_image = get_base64_image(BACKGROUND_FILE)

        background_css = f"""
        background-color: #2b1a10;
        background-image: url("data:image/png;base64,{background_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-position: top center;
        background-attachment: fixed;
        """
    else:
        background_css = "background-color: #2b1a10;"

    st.markdown(
        f"""
        <style>

        .stApp {{
            {background_css}
        }}

        .main .block-container {{
            background-color: rgba(236, 207, 150, 0.00);
            border-radius: 18px;
            padding: 2rem;
            max-width: 950px;
        }}

        .logo-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 1rem;
        }}

        .slogan {{
            font-family: "Courier New", monospace;
            font-size: 1.25rem;
            font-weight: 700;
            line-height: 1.7;
            color: #2b1a10;
            margin-top: 0.5rem;
            margin-bottom: 2rem;
        }}

        h1, h2, h3 {{
            font-family: "Times New Roman", serif !important;
            color: #2b1a10 !important;
            font-weight: 700 !important;
        }}

        h2 {{
            font-size: 2.2rem !important;
        }}

        p, div, label, span {{
            color: #2b1a10;
        }}

        label,
        .stMarkdown,
        .stCaption {{
            font-family: "Courier New", monospace !important;
            font-size: 1rem !important;
            font-weight: 500 !important;
            color: #2b1a10 !important;
        }}

        p,
        div {{
            font-family: "Courier New", monospace;
        }}

        input,
        textarea {{
            background-color: rgba(59, 36, 20, 0.78) !important;
            color: #f8e7bd !important;
            caret-color: #f8e7bd !important;
            border: 1px solid #8a613a !important;
            border-radius: 10px !important;
        }}

        input::placeholder,
        textarea::placeholder {{
            color: #d7bd88 !important;
        }}

        .stSelectbox div[data-baseweb="select"] > div {{
            background-color: rgba(59, 36, 20, 0.78) !important;
            color: #f8e7bd !important;
            border: 1px solid #8a613a !important;
            border-radius: 10px !important;
        }}

        .stSelectbox div[data-baseweb="select"] span {{
            color: #f8e7bd !important;
        }}

        .stNumberInput input,
        .stTextInput input,
        .stTextArea textarea {{
            background-color: rgba(59, 36, 20, 0.78) !important;
            color: #f8e7bd !important;
        }}

        .stButton > button {{
            background-color: rgba(59, 36, 20, 0.88);
            color: #f8e7bd;
            border-radius: 10px;
            border: 1px solid #8a613a;
            padding: 0.6rem 1rem;
            font-weight: bold;
            font-family: "Courier New", monospace;
        }}

        .stButton > button:hover {{
            background-color: rgba(90, 56, 34, 0.95);
            color: #fff1c7;
            border: 1px solid #b8874f;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    """Run the Rough Draught Streamlit app."""
    st.set_page_config(
        page_title="Rough Draught",
        page_icon="🍺",
        layout="centered",
    )

    load_custom_css()

    if LOGO_FILE.exists():
        st.markdown('<div class="logo-container">', unsafe_allow_html=True)
        st.image(str(LOGO_FILE), width=420)
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(
    """
    <div class="slogan">
        Track the good taps and the rough draughts.<br>
        Never re-buy a bad beer again!
    </div>
    """,
    unsafe_allow_html=True,
    )   

    st.markdown(
        """
        <h2 style="
            font-family: 'Courier New', monospace;
            color: #2b1a10;
            font-weight: 700;
        ">
            Add a Beer Entry
        </h2>
        """,
        unsafe_allow_html=True,
    )

    with st.form("beer_entry_form"):
        location = st.text_input(
            "Location Purchased/Consumed "
            "(Optional: store, brewery, bar, restaurant)"
        )

        beer_name = st.text_input(
            "Beer Name :red[*] "
            "(Required: use the name on the label or menu)"
        )

        brewery = st.text_input(
            "Brewery :red[*] "
            "(Required: who made it?)"
        )

        style_choice = st.selectbox(
            "Beer Style",
            options=list(STYLE_OPTIONS.keys()),
            format_func=lambda x: f"{x}. {STYLE_OPTIONS[x]}",
        )
        beer_style = STYLE_OPTIONS[style_choice]

        if beer_style == "Other":
            beer_style = st.text_input("Enter Beer Style")

        abv = st.number_input(
            "ABV % (Optional: leave at 0 if unknown)",
            min_value=0.0,
            max_value=50.0,
            value=0.0,
            step=0.1,
        )

        strength = determine_strength(abv)
        st.caption(f"Strength Category: {strength}")

        country_choice = st.selectbox(
            "Country of Origin",
            options=list(COUNTRY_OPTIONS.keys()),
            format_func=lambda x: f"{x}. {COUNTRY_OPTIONS[x]}",
        )
        country = COUNTRY_OPTIONS[country_choice]

        city = ""
        state = ""

        if country == "United States":
            city = st.text_input("Brewery City")
            state = st.text_input("Brewery State")
        elif country == "Other":
            country = st.text_input("Enter Country")

        pack_size_choice = st.selectbox(
            "Pack Size",
            options=list(PACK_SIZE_OPTIONS.keys()),
            format_func=lambda x: f"{x}. {PACK_SIZE_OPTIONS[x]}",
        )
        pack_size = PACK_SIZE_OPTIONS[pack_size_choice]

        if pack_size == "Other":
            pack_size = st.text_input("Enter Pack Size")

        container_size = ""

        if pack_size != "Draught Pour":
            container_size_choice = st.selectbox(
                "Bottle/Can Size",
                options=list(CONTAINER_SIZE_OPTIONS.keys()),
                format_func=lambda x: f"{x}. {CONTAINER_SIZE_OPTIONS[x]}",
            )
            container_size = CONTAINER_SIZE_OPTIONS[container_size_choice]

            if container_size == "Other":
                container_size = st.text_input("Enter Bottle/Can Size")
        else:
            container_size = "Draught Pour"

        price = st.number_input(
            "Price Paid ($)",
            min_value=0.0,
            max_value=500.0,
            value=0.0,
            step=0.50,
        )

        buy_again = st.radio(
            "Would you buy this again?",
            ["Yes", "No"],
            horizontal=True,
        )

        rating = st.slider(
            "Your Rating",
            min_value=1,
            max_value=5,
            value=3,
        )

        rating_description = RATING_DESCRIPTIONS[rating]
        st.caption(f"Rating Meaning: {rating_description}")

        tasting_notes = st.text_area(
            "What flavors are YOU getting? "
            "(Optional: aroma, taste, mouthfeel, finish, or anything memorable)"
        )

        submitted = st.form_submit_button("Save Beer")

        if submitted:
            errors = []

            errors.extend(validate_required_fields(beer_name, brewery))

            style_error = validate_style_choice(style_choice)
            country_error = validate_country_choice(country_choice)
            pack_size_error = validate_pack_size_choice(pack_size_choice)
            abv_error = validate_abv(abv)
            price_error = validate_price(price)

            if style_error:
                errors.append(style_error)

            if country_error:
                errors.append(country_error)

            if pack_size_error:
                errors.append(pack_size_error)

            if abv_error:
                errors.append(abv_error)

            if price_error:
                errors.append(price_error)

            if beer_style == "Other":
                errors.append(validate_other_field(beer_style, "Beer style"))

            if country_choice == 8:
                errors.append(validate_other_field(country, "Country"))

            if pack_size_choice == 7:
                errors.append(validate_other_field(pack_size, "Pack size"))

            if pack_size != "Draught Pour":
                container_size_error = validate_container_size_choice(
                    container_size_choice
                )

                if container_size_error:
                    errors.append(container_size_error)

                if container_size_choice == 6:
                    errors.append(
                        validate_other_field(
                            container_size,
                            "Bottle/Can size",
                        )
                    )

            if country == "United States":
                errors.extend(validate_us_location(city, state))

            errors = [error for error in errors if error]

            if errors:
                for error in errors:
                    st.error(error)
            else:
                entry = BeerEntry(
                    timestamp=datetime.now(CENTRAL_TIME).strftime(
                        "%Y-%m-%d %I:%M %p %Z"
                    ),
                    location=location.strip(),
                    beer_name=beer_name.strip(),
                    brewery=brewery.strip(),
                    beer_style=beer_style.strip(),
                    abv=abv,
                    strength=strength,
                    country=country.strip(),
                    city=city.strip(),
                    state=state.strip(),
                    pack_size=pack_size.strip(),
                    container_size=container_size.strip(),
                    price=price,
                    buy_again=buy_again,
                    rating=rating,
                    rating_description=rating_description,
                    tasting_notes=tasting_notes.strip(),
                )

                save_entry(entry)
                st.success(f"Saved: {entry.summary()}")

    st.header("Saved Beer Entries")

    entries = load_entries()

    search_term = st.text_input("Search entries")

    if search_term:
        search_term = search_term.lower().strip()
        entries = entries[
            entries.apply(
                lambda row: search_term
                in row.astype(str).str.lower().to_string(),
                axis=1,
            )
        ]

    if entries.empty:
        st.info("No beer entries found yet.")
    else:
        st.dataframe(entries, use_container_width=True)

        st.subheader("Expanded Tasting Notes")

        for _, row in entries.iterrows():
            with st.expander(f"{row['beer_name']} by {row['brewery']}"):
                notes = row["tasting_notes"]

                if pd.isna(notes) or str(notes).strip() == "":
                    st.write("No tasting notes entered.")
                else:
                    st.write(notes)


if __name__ == "__main__":
    main()