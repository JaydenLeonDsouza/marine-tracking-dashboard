from folium.plugins import MarkerCluster
import streamlit as st
import pandas as pd
import psycopg2
import folium
from streamlit_folium import st_folium

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    database="marine",
    user="postgres",
    password="jlds",
    port="5432"
)

# Load ship data
query = """
SELECT vessel_name, latitude, longitude, sog
FROM ship_positions
LIMIT 100;
"""

df = pd.read_sql(query, conn)

conn.close()

# Streamlit title
st.title("🚢 Marine Tracking Dashboard")

st.write(f"Loaded {len(df)} ships")

# Create map
m = folium.Map(location=[20, 0], zoom_start=2)

# Create marker cluster layer
marker_cluster = MarkerCluster().add_to(m)

# Add ship markers
for _, row in df.iterrows():

    vessel = row["vessel_name"]

    if pd.isna(vessel):
        vessel = "Unknown Vessel"

    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=5,
        popup=f"""
        <b>{vessel}</b><br>
        Speed: {row['sog']} knots
        """,
        fill=True
    ).add_to(marker_cluster)

# Render map
st_folium(m, width=1200, height=700)