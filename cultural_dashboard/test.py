import streamlit as st
import snowflake.connector
import pandas as pd

# Snowflake Connection
conn = snowflake.connector.connect(
    user='YOUR_USERNAME',
    password='YOUR_PASSWORD',
    account='YOUR_ACCOUNT',
    warehouse='YOUR_WAREHOUSE',
    database='YOUR_DATABASE',
    schema='YOUR_SCHEMA'
)

# Run query
def run_query(query):
    cur = conn.cursor()
    cur.execute(query)
    return cur.fetchall()

# Sample query
data = run_query("SELECT state, tourist_count FROM tourism_data;")
df = pd.DataFrame(data, columns=["State", "Tourist Count"])

# Display in Streamlit
st.title("Cultural Tourism Trends")
st.bar_chart(df.set_index("State"))
