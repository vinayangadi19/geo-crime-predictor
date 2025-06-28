import streamlit as st
import pandas as pd
import joblib
import folium
from streamlit_folium import st_folium

# Load model & encoder
model = joblib.load("model/crime_model.pkl")
label_encoder = joblib.load("model/label_encoder.pkl")

st.set_page_config(page_title="Geo-Crime Predictor", layout="centered")

st.title("🚨 Geo-Crime Predictor")
st.markdown("Predict crime risk based on your location coordinates.")

# Map input
st.subheader("📍 Select your location on the map or enter manually")

default_lat = 17.3850
default_lon = 78.4867

m = folium.Map(location=[default_lat, default_lon], zoom_start=12)
marker = folium.Marker([default_lat, default_lon], draggable=True)
marker.add_to(m)

map_data = st_folium(m, height=350, width=700)

# Read lat/lon from map OR manual input
if map_data and map_data["last_clicked"]:
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
else:
    lat = st.number_input("Latitude", value=default_lat, format="%.6f")
    lon = st.number_input("Longitude", value=default_lon, format="%.6f")

# Predict button
if st.button("🔍 Predict Crime Risk"):
    input_df = pd.DataFrame([[lat, lon]], columns=["latitude", "longitude"])
    pred = model.predict(input_df)[0]
    label = label_encoder.inverse_transform([pred])[0]
    st.success(f"Predicted Crime Risk Level: **{label}**")
