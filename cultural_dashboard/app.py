import streamlit as st
import altair as alt
import pandas as pd
from data_loader import (
    load_tourism_data,
    load_culture_budget,
    load_monument_footfall,
)

st.set_page_config(page_title="Cultural Tourism in India", layout="wide")
import streamlit as st
import altair as alt
import pandas as pd
from data_loader import (
    load_tourism_data,
    load_culture_budget,
    load_monument_footfall,
)

st.set_page_config(page_title="India Cultural Dashboard", layout="wide")

st.title("🇮🇳 India's Cultural Tourism & Heritage Explorer")

tab1, tab2, tab3 = st.tabs(["📊 Tourism Trends", "💰 Budget Growth", "🗺️ Monument Footfall"])

# --- TAB 1: TOURISM ---
with tab1:
    st.header("Tourism Trends (Domestic vs Foreign)")
    tourism_df = load_tourism_data()

    state = st.selectbox("Select a State", sorted(tourism_df['state'].unique()))
    state_data = tourism_df[tourism_df['state'] == state]

    col1, col2 = st.columns(2)
    with col1:
        dom_chart = alt.Chart(state_data).mark_line(point=True).encode(
            x="year:O",
            y="domestic_visits:Q",
            tooltip=["year", "domestic_visits"]
        ).properties(title="Domestic Visits")

        st.altair_chart(dom_chart, use_container_width=True)

    with col2:
        for_chart = alt.Chart(state_data).mark_line(point=True, color="crimson").encode(
            x="year:O",
            y="foreign_visits:Q",
            tooltip=["year", "foreign_visits"]
        ).properties(title="Foreign Visits")

        st.altair_chart(for_chart, use_container_width=True)

# --- TAB 2: BUDGET ---
with tab2:
    st.header("Culture Ministry Budget Over Years")
    budget_df = load_culture_budget()

    bar = alt.Chart(budget_df).mark_bar().encode(
        x=alt.X("year:O", title="Year"),
        y=alt.Y("budget_inr_cr:Q", title="Budget (INR Cr)"),
        tooltip=["year", "budget_inr_cr"]
    ).properties(title="Ministry of Culture Budget")

    st.altair_chart(bar, use_container_width=True)

# --- TAB 3: MONUMENT FOOTFALL ---
with tab3:
    st.header("Footfall at Major Cultural Monuments")
    monument_df = load_monument_footfall()

    st.dataframe(monument_df)

    st.markdown("### 📍 Map of Select Cultural Sites (Example Coordinates)")
    site_map = pd.DataFrame({
        "lat": [27.1751, 15.3219, 19.8876],
        "lon": [78.0421, 75.7804, 86.0945],
        "site": ["Taj Mahal", "Hampi", "Konark Sun Temple"]
    })
    st.map(site_map)

    st.markdown("### 📈 Footfall by Monument")
    bar = alt.Chart(monument_df).mark_bar().encode(
        x=alt.X("site_name:N", sort='-y'),
        y=alt.Y("visitors:Q"),
        color="unesco_site:N",
        tooltip=["site_name", "visitors"]
    ).properties(title="Visitor Numbers")

    st.altair_chart(bar, use_container_width=True)

st.title("🇮🇳 Cultural Tourism & Heritage Dashboard")

tab1, tab2, tab3 = st.tabs(["📊 Tourism Trends", "💰 Culture Budget", "🗺️ Monument Footfall"])

# TAB 1: TOURISM TRENDS
with tab1:
    st.subheader("Domestic & Foreign Tourism Visits by State and Year")
    tourism_df = load_tourism_data()

    state_option = st.selectbox("Choose a State:", sorted(tourism_df["state"].unique()))
    filtered = tourism_df[tourism_df["state"] == state_option]

    c1 = alt.Chart(filtered).mark_line(point=True).encode(
        x="year:O",
        y=alt.Y("domestic_visits:Q", title="Domestic Visits"),
        tooltip=["year", "domestic_visits"]
    ).properties(title=f"{state_option} - Domestic Tourism")

    c2 = alt.Chart(filtered).mark_line(point=True, color='red').encode(
        x="year:O",
        y=alt.Y("foreign_visits:Q", title="Foreign Visits"),
        tooltip=["year", "foreign_visits"]
    ).properties(title=f"{state_option} - Foreign Tourism")

    st.altair_chart(c1 | c2, use_container_width=True)

# TAB 2: CULTURE BUDGET
with tab2:
    st.subheader("Ministry of Culture - Annual Budget (INR Crores)")
    budget_df = load_culture_budget()

    chart = alt.Chart(budget_df).mark_bar().encode(
        x="year:O",
        y="budget_inr_cr:Q",
        tooltip=["year", "budget_inr_cr"]
    ).properties(title="Budget Growth Over Time")

    st.altair_chart(chart, use_container_width=True)

# TAB 3: MONUMENT FOOTFALL
with tab3:
    st.subheader("Major Cultural Sites - Visitor Footfall (2022)")
    monument_df = load_monument_footfall()

    st.dataframe(monument_df)

    st.markdown("### Map View of Cultural Monuments")
    try:
        import geopandas as gpd
    except ImportError:
        st.warning("Install `geopandas` for enhanced map capabilities.")
    else:
        # Use basic geolocation map if coordinates were added
        site_map = pd.DataFrame({
            "lat": [27.1751, 20.0268, 19.8876],
            "lon": [78.0421, 75.1791, 86.0945],
            "site_name": ["Taj Mahal", "Ellora Caves", "Sun Temple"]
        })
        st.map(site_map)

    bar = alt.Chart(monument_df).mark_bar().encode(
        x=alt.X("site_name:N", sort="-y", title="Monument"),
        y=alt.Y("visitors:Q", title="Visitors"),
        color="unesco_site:N",
        tooltip=["site_name", "visitors"]
    ).properties(title="Footfall by Monument")

    st.altair_chart(bar, use_container_width=True)
