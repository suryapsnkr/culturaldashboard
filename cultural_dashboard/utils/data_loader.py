import snowflake.connector
import pandas as pd
import streamlit as st

@st.cache_data(show_spinner=False)
def get_snowflake_connection():
    return snowflake.connector.connect(
        user=st.secrets["snowflake"]["user"],
        password=st.secrets["snowflake"]["password"],
        account=st.secrets["snowflake"]["account"],
        warehouse=st.secrets["snowflake"]["warehouse"],
        database=st.secrets["snowflake"]["database"],
        schema=st.secrets["snowflake"]["schema"]
    )

@st.cache_data(show_spinner=False)
def load_data(query):
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        return cursor.fetch_pandas_all()
    finally:
        cursor.close()
        conn.close()

def load_tourism_data():
    return load_data("SELECT * FROM tourism_visits")

def load_culture_budget():
    return load_data("SELECT * FROM culture_budget")

def load_monument_footfall():
    return load_data("SELECT * FROM monument_footfall")
