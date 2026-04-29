"""
Rough Draught Streamlit App
MVP v1: Create, save, view, and search beer tasting entries.
"""

from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st


DATA_DIR = Path("data")
DATA_FILE = DATA_DIR / "beer_entries.csv"
CENTRAL_TIME = ZoneInfo("America/Chicago")


def ensure_data_file():
    """Create the data folder and CSV file if they do not exist."""
    DATA_DIR.mkdir(exist_ok=True)

    if not DATA_FILE.exists():
        df = pd.DataFrame(
            columns=[
                "timestamp",
                "store",
                "beer_name",
                "brewery",
                "abv",
                "region",
                "rating",
                "tasting_notes",
            ]
        )
        df.to_csv(DATA_FILE, index=False)


def load_entries():
    """Load beer entries from the CSV file"""
    ensure_data_file()
    return pd.read_csv(DATA_FILE)


def save_entry(entry):
    """Save a new beer entry to the CSV file"""
    df = load_entries()
    new_entry = pd.DataFrame([entry])
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(DATA_FILE, index=False)


def main():
    """Run the Rough Draught Streamlit app."""
    st.set_page_config(page_title="Rough Draught", page_icon="🍺")

    st.title("🍺 Rough Draught 🍺")
    st.write("Track beers you have tried, where you bought them, and what you thought.")

    st.header("Add a Beer Entry")

    with st.form("beer_entry_form"):
        store = st.text_input("Store Purchased From")
        beer_name = st.text_input("Beer Name")
        brewery = st.text_input("Brewery")
        abv = st.number_input("ABV %", min_value=0.0, max_value=25.0, step=0.1)
        region = st.text_input("Region")
        rating = st.slider("Rating", min_value=0, max_value=10, value=0)
        tasting_notes = st.text_area("Tasting Notes")

        submitted = st.form_submit_button("Save Beer")

        if submitted:
            if not beer_name or not brewery:
                st.error("Beer name and brewery are required.")
            else:
                entry = {
                    "timestamp": datetime.now(CENTRAL_TIME).strftime(
                    "%Y-%m-%d %I:%M %p %Z"
                    ),
                    "store": store,
                    "beer_name": beer_name,
                    "brewery": brewery,
                    "abv": abv,
                    "region": region,
                    "rating": rating,
                    "tasting_notes": tasting_notes,
                }

                save_entry(entry)
                st.success(f"Saved: {beer_name} by {brewery}")

    st.header("Saved Beer Entries")

    entries = load_entries()

    search_term = st.text_input("Search entries")

    if search_term:
        search_term = search_term.lower()
        entries = entries[
            entries.apply(
                lambda row: search_term in row.astype(str).str.lower().to_string(),
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
                st.write(row["tasting_notes"])


if __name__ == "__main__":
    main()