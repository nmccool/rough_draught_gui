"""
Rough Draught Streamlit App
MVP v2: Create, save, view, and search beer tasting entries.
"""

import base64
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st

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

ASSETS_DIR = BASE_DIR / "Assets"
DATA_DIR = BASE_DIR / "data"

LOGO_FILE = ASSETS_DIR / "RoughDraughtLogoT.png"
BACKGROUND_FILE = ASSETS_DIR / "Notepad.png"

DATA_FILE = DATA_DIR / "beer_entries.csv"

CENTRAL_TIME = ZoneInfo("America/Chicago")


ENTRY_COLUMNS = [
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


def get_base64_image(image_path):
    """Convert an image file to base64 for CSS use (going next level)"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def ensure_data_file():
    """Create the data folder and CSV file if they do not exist"""
    DATA_DIR.mkdir(exist_ok=True)

    if not DATA_FILE.exists():
        df = pd.DataFrame(columns=ENTRY_COLUMNS)
        df.to_csv(DATA_FILE, index=False)


def load_entries():
    """Load beer entries from the CSV file"""
    ensure_data_file()
    df = pd.read_csv(DATA_FILE)

    for column in ENTRY_COLUMNS:
        if column not in df.columns:
            df[column] = ""

    return df[ENTRY_COLUMNS]


def save_entry(entry):
    """Save a new beer entry to the CSV file"""
    df = load_entries()
    new_entry = pd.DataFrame([entry.to_dict()])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)


def load_custom_css():
    """Adding my own theme to the app (this is my wheelhouse)"""
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
        header {{
            visibility: hidden;
        }}

        .stApp {{
            {background_css}
        }}

        .block-container {{
            padding-top: 1rem !important;
            padding-bottom: 2rem;
            padding-left: 7rem;
            padding-right: 2rem;
            max-width: 675px;
        }}

        .slogan {{
            font-family: "Courier New", monospace;
            font-size: 1.25rem;
            font-weight: 700;
            line-height: 1;
            color: #2b1a10;
            text-align: center;
            margin-top: -1rem;
            margin-bottom: 0rem;
        }}

        .custom-header {{
            font-family: "Courier New", monospace !important;
            color: #2b1a10 !important;
            font-size: 1.25rem !important;
            font-weight: 700 !important;
            margin-top: 1rem !important;
            margin-left: 1rem !important;
            margin-bottom: -1.25rem !important;
        }}

        p, div, label, span {{
            color: #2b1a10;
        }}

        label,
        .stMarkdown,
        .stCaption {{
            font-family: "Courier New", monospace !important;
            font-weight: bold;
            font-size: 1rem !important;
            font-weight: 500 !important;
            color: #f8e7bd !important;
        }}

        p, div {{
            font-family: "Courier New", monospace;
            font-weight: bold;
        }}

        input,
        textarea {{
            background-color: rgba(59, 36, 20, 0.60) !important;
            color: #f8e7bd !important;
            caret-color: rgba(59, 36, 20, 0.60) !important;
            border: 0px solid #2b1a10 !important;
            border-radius: 10px !important;
        }}

        input::placeholder,
        textarea::placeholder {{
            color: #f8e7bd !important;
        }}

        .stSelectbox div[data-baseweb="select"] > div {{
            background-color: rgba(59, 36, 20, 0.60) !important;
            color: #f8e7bd !important;
            border: 1px solid #2b1a10 !important;
            border-radius: 10px !important;
        }}

        .stSelectbox div[data-baseweb="select"] span {{
            color: #f8e7bd !important;
        }}

        /* Dropdown menu background */
        div[role="listbox"] {{
            background-color: rgba(59, 36, 20, 0.60) !important;
            border: 1px solid #8a613a !important;
        }}

        /* Individual dropdown options */
        div[role="option"] {{
            background-color: rgba(59, 36, 20, 0.60) !important;
            color: #f8e7bd !important;
            font-family: "Courier New", monospace !important;
        }}

        /* Hovered option */
        div[role="option"]:hover {{
            background-color: rgba(59, 36, 20, 0.60) !important;
            color: #fff1c7 !important;
        }}

        /* Selected option */
        div[aria-selected="true"] {{
            background-color: rgba(59, 36, 20, 0.60) !important;
            color: #fff1c7 !important;
        }}
        .stTextInput input,
        .stTextArea textarea {{
            background-color: #7f6342 !important;
            color: #f8e7bd !important;
        }}
        [data-baseweb="input"] {{
            background-color: rgba(59, 36, 20, 0.60) !important;
        }}

        .stRadio label,
        .stRadio div {{
            color: #2b1a10 !important;
            font-family: "Courier New", monospace !important;
            font-weight: bold;
        }}

        div[data-testid="stFormSubmitButton"] button {{
            background-color: #7f6342 !important;
            color: #f8e7bd !important;
            border: 1px solid #8a613a !important;
            border-radius: 10px !important;
            padding: 0.65rem 1.25rem !important;
            font-family: "Courier New", monospace !important;
            font-weight: bold;
            font-size: 1rem !important;
            font-weight: 700 !important;
        }}

        div[data-testid="stFormSubmitButton"] button:hover {{
            background-color: rgba(90, 56, 34, 0.95) !important;
            color: #fff1c7 !important;
            border: 1px solid #8a613a !important;
        }}

        div[data-testid="stFormSubmitButton"] button:focus {{
            color: #fff1c7 !important;
            border: 1px solid #8a613a !important;
            box-shadow: 0 0 0 2px rgba(184, 135, 79, 0.35) !important;
        }}

        
        /* Dropdown options */
        li[role="option"],
        div[role="option"] {{
            background-color: #7f6342 !important;
            color: #f8e7bd !important;
        }}

        /* Hover/focus option */
        li[role="option"]:hover,
        div[role="option"]:hover,
        li[aria-selected="true"],
        div[aria-selected="true"] {{
            background-color: #9a7a53 !important;
            color: #fff1c7 !important;
        }}

        /* Placeholder/value text */
        div[data-baseweb="select"] * {{
            color: #f8e7bd !important;
            -webkit-text-fill-color: #f8e7bd !important;
        }}

        div[data-baseweb="select"] input {{
            caret-color: transparent !important;
        }}

        /* TRUE NUCLEAR TEXT COLOR OVERRIDE */
        div[data-baseweb="select"] *,
        div[data-baseweb="popover"] *,
        div[data-baseweb="menu"] *,
        div[role="listbox"] *,
        div[role="option"] *,
        li[role="option"] * {{
            color: #f8e7bd !important;
            -webkit-text-fill-color: #f8e7bd !important;
        }}

        /* NUCLEAR CURSOR KILL */

        div[data-baseweb="select"] input,
        div[data-baseweb="select"] textarea {{
            caret-color: transparent !important;
            color: transparent !important;
            text-shadow: 0 0 0 #f8e7bd !important;
        }}

        div[data-baseweb="select"] input:focus {{
            outline: none !important;
            box-shadow: none !important;
        }}

        /* SAVE BUTTON NUCLEAR OVERRIDE */

        div[data-testid="stFormSubmitButton"] button,
        button[kind="primaryFormSubmit"] {{
            background-color: #7f6342 !important;
            color: #f8e7bd !important;
            -webkit-text-fill-color: #f8e7bd !important;

            border: 1px solid #8a613a !important;
            border-radius: 10px !important;

            font-family: "Courier New", monospace !important;
            font-size: 1rem !important;
            font-weight: 700 !important;

            padding: 0.65rem 1.25rem !important;

            box-shadow: none !important;
        }}

        /* EVERYTHING INSIDE BUTTON */
        div[data-testid="stFormSubmitButton"] button *,
        button[kind="primaryFormSubmit"] * {{
            color: #f8e7bd !important;
            -webkit-text-fill-color: #f8e7bd !important;
        }}

        /* Hover */
        div[data-testid="stFormSubmitButton"] button:hover,
        button[kind="primaryFormSubmit"]:hover {{
            background-color: #9a7a53 !important;
            color: #fff1c7 !important;
            border-color: #b8874f !important;
        }}

        /* Hover text */
        div[data-testid="stFormSubmitButton"] button:hover *,
        button[kind="primaryFormSubmit"]:hover * {{
            color: #fff1c7 !important;
            -webkit-text-fill-color: #fff1c7 !important;
        }}

        .empty-message {{
        font-family: "Courier New", monospace;
        color: #2b1a10;
        font-size: 1.1rem;
        margin-top: 1rem;
        padding-left: 7rem;
        padding-right: 2rem;
        }}

        .search-box {{
        padding-left: 7rem;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    """Run the Rough Draught Streamlit app"""
    st.set_page_config(
        page_title="Rough Draught",
        page_icon="🍺",
        layout="centered",
    )

    load_custom_css()

    _, center_col, _ = st.columns([1, 2, 1])

    with center_col:
        if LOGO_FILE.exists():
            st.image(str(LOGO_FILE), width=420)

    st.markdown(
        """
        <div class="slogan">
            Track the good taps and the rough draughts.<br>
            So you never re-buy a bad beer again!
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="custom-header">
               Log a Beer
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("beer_entry_form"):
        beer_name = st.text_input(
            "Beer Name:red[*] (Required)"
        )

        brewery = st.text_input(
            "Brewery:red[*] (Required)"
        )

        col1, col2 = st.columns(2)

        with col1:
            style_choice = st.selectbox(
                "Beer Style",
                options=list(STYLE_OPTIONS.keys()),
                format_func=lambda x: STYLE_OPTIONS[x],
            )
            beer_style = STYLE_OPTIONS[style_choice]

            if beer_style == "Other":
                beer_style = st.text_input("Enter Beer Style")

        with col2:
            abv_input = st.text_input(
                "ABV% (Enter 0 if unknown)",
                value="",
            )

        col3, col4 = st.columns(2)

        with col3:
            country_choice = st.selectbox(
                "Country",
                options=list(COUNTRY_OPTIONS.keys()),
                format_func=lambda x: COUNTRY_OPTIONS[x],
            )
            country = COUNTRY_OPTIONS[country_choice]

            if country == "Other":
                country = st.text_input("Enter Country")

        location_detail = ""

        with col4:
            if country == "United States":
                location_detail = st.text_input(
                    "City, State",
                    placeholder="Example: Chicago, IL",
                )
            else:
                st.text_input(
                    "City, State",
                    value="Not required outside United States",
                    disabled=True,
                )

        col5, col6 = st.columns(2)

        with col5:
            pack_size_choice = st.selectbox(
                "Pack Size",
                options=list(PACK_SIZE_OPTIONS.keys()),
                format_func=lambda x: PACK_SIZE_OPTIONS[x],
            )
            pack_size = PACK_SIZE_OPTIONS[pack_size_choice]

            if pack_size == "Other":
                pack_size = st.text_input("Enter Pack Size")

        with col6:
            container_size = ""
            container_size_choice = None

            if pack_size != "Draught Pour":
                container_size_choice = st.selectbox(
                    "Bottle/Can Size",
                    options=list(CONTAINER_SIZE_OPTIONS.keys()),
                    format_func=lambda x: CONTAINER_SIZE_OPTIONS[x],
                )
                container_size = CONTAINER_SIZE_OPTIONS[container_size_choice]

                if container_size == "Other":
                    container_size = st.text_input("Enter Bottle/Can Size")
            else:
                container_size = "Draught Pour"
                st.text_input(
                    "Bottle/Can Size",
                    value="Not needed for draught pour",
                    disabled=True,
                )

        col7, col8 = st.columns(2)

        with col7:
            price_input = st.text_input(
                "Price (Enter 0 if unknown)",
                value="",
            )

        with col8:
            buy_again = st.radio(
                "Would Buy Again?",
                ["Yes", "No"],
                horizontal=True,
            )

        rating = st.selectbox(
            "Rating",
            options=list(RATING_DESCRIPTIONS.keys()),
            format_func=lambda x: RATING_DESCRIPTIONS[x],
        )

        rating_description = RATING_DESCRIPTIONS[rating]

        tasting_notes = st.text_area(
            "What flavors are YOU getting?\n"
            "\n(Aromas, flavors, mouthfeel, finish, or anything memorable)"
        )

        submitted = st.form_submit_button("Save Beer")

        if submitted:
            errors = []

            try:
                abv = float(abv_input)
            except ValueError:
                abv = -1
                errors.append("ABV must be a number.")

            try:
                price = float(price_input)
            except ValueError:
                price = -1
                errors.append("Price must be a number.")

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

            if style_choice == 10:
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
                if not location_detail.strip():
                    errors.append(
                        "Please enter the city and state for the brewery."
                    )

            errors = [error for error in errors if error]

            if errors:
                for error in errors:
                    st.error(error)
            else:
                strength = determine_strength(abv)

                entry = BeerEntry(
                    timestamp=datetime.now(CENTRAL_TIME).strftime(
                        "%Y-%m-%d %I:%M %p %Z"
                    ),
                    location="",
                    beer_name=beer_name.strip(),
                    brewery=brewery.strip(),
                    beer_style=beer_style.strip(),
                    abv=abv,
                    strength=strength,
                    country=country.strip(),
                    city=location_detail.strip(),
                    state="",
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

    st.markdown(
    """
    <div class="custom-header">
        Saved Beer Entries
    </div>
    """,
    unsafe_allow_html=True,
    )
    st.markdown("<br>", unsafe_allow_html=True)

    entries = load_entries()
    
    left_spacer, search_col, right_spacer = st.columns([0.2, 5, 1])

    with search_col:
        search_term = st.text_input(
        "Search Entries",
        placeholder="Search brewery, beer, style, notes...",
        )


        st.markdown(
            '</div>',
            unsafe_allow_html=True,
        )

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
        st.markdown(
        """
        <div class="empty-message">
            No beer entries found yet.
        </div>
        """,
        unsafe_allow_html=True,
        )
    else:
        display_columns = [
            "beer_name",
            "brewery",
            "beer_style",
            "abv",
            "strength",
            "rating",
            "buy_again",
        ]

        st.dataframe(
            entries[display_columns],
            use_container_width=True,
        )

        st.subheader("Expanded Tasting Notes")

        for _, row in entries.iterrows():
            with st.expander(f"{row['beer_name']} by {row['brewery']}"):
                notes = row["tasting_notes"]

                st.write(f"Style: {row['beer_style']}")
                st.write(f"ABV: {row['abv']}%")
                st.write(f"Strength: {row['strength']}")
                st.write(f"Country: {row['country']}")
                st.write(f"City: {row['city']}")
                st.write(f"State: {row['state']}")
                st.write(f"Pack Size: {row['pack_size']}")
                st.write(f"Bottle/Can Size: {row['container_size']}")
                st.write(f"Price: ${row['price']}")
                st.write(f"Buy Again: {row['buy_again']}")
                st.write(f"Rating: {row['rating']}/5")
                st.write(f"Rating Meaning: {row['rating_description']}")

                if pd.isna(notes) or str(notes).strip() == "":
                    st.write("No tasting notes entered.")
                else:
                    st.write(f"Tasting Notes: {notes}")


if __name__ == "__main__":
    main()