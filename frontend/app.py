import streamlit as st
import requests
from PIL import Image



# Load the banner image
banner_image = Image.open("soulmate.png")

# Display the banner image at the top of the page
st.image(banner_image, width=800)  # Adjust the width as needed


# Streamlit UI
st.title("Personal Birth Information Prediction")

# Create two columns for user input sections
col1, col2 = st.columns(2)

# User Input (First Set)
with col1:
    st.header("First Person")
    day1 = st.text_input("Day")
    month1 = st.text_input("Month")
    year1 = st.text_input("Year")
    hour1 = st.text_input("Hour")
    minute1 = st.text_input("Minute")
    latitude1 = st.text_input("Latitude")
    longitude1 = st.text_input("Longitude")
    timezone1 = st.text_input("Timezone")

# User Input (Second Set)
with col2:
    st.header("Second person")
    day2 = st.text_input("Day ")
    month2 = st.text_input("Month ")
    year2 = st.text_input("Year ")
    hour2 = st.text_input("Hour ")
    minute2 = st.text_input("Minute ")
    latitude2 = st.text_input("Latitude ")
    longitude2 = st.text_input("Longitude ")
    timezone2 = st.text_input("Timezone ")

# Make POST requests to the FastAPI model when the single "Get Predictions" button is clicked
if st.button("Get Predictions"):
    api_url = "http://localhost:8001/astroinfo"  # Change to the actual FastAPI endpoint URL
    
    user_input1 = {
        "day": day1,
        "month": month1,
        "year": year1,
        "hour": hour1,
        "min": minute1,
        "lat": latitude1,
        "lon": longitude1,
        "tzone": timezone1,
    }
    
    user_input2 = {
        "day": day2,
        "month": month2,
        "year": year2,
        "hour": hour2,
        "min": minute2,
        "lat": latitude2,
        "lon": longitude2,
        "tzone": timezone2,
    }
    
    response1 = requests.post(api_url, json=user_input1)
    response2 = requests.post(api_url, json=user_input2)

    if response1.status_code == 200 and response2.status_code == 200:
        prediction1 = response1.json()
        prediction2 = response2.json()
        st.success(f"Prediction (First Set): {prediction1}")
        st.success(f"Prediction (Second Set): {prediction2}")
    else:
        st.error("Error occurred while making the predictions.")

        