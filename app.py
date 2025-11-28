import streamlit as st
import requests
from datetime import datetime, time, date

# ----------------- PAGE CONFIG -----------------
st.set_page_config(
    page_title="Taxi Fare Estimator",
    page_icon="🚕",
    layout="centered",
    initial_sidebar_state="collapsed",
)

## Here we would like to add some controllers in order to ask the user to select the parameters of the ride

# st.markdown('''
# - date and time:  `st.date_input` + `st.time_input`
# - pickup longitude: `st.number_input`
# - pickup latitude: `st.number_input`
# - dropoff longitude: `st.number_input`
# - dropoff latitude: `st.number_input`
# - passenger count: `st.number_input`)
# ''')

date = st.date_input("Pickup Date")
time = st.time_input("Pickup Time")
pickup_longitude = st.number_input("Pickup Longitude", value=-73.985428)
pickup_latitude = st.number_input("Pickup Latitude", value=40.748817)
dropoff_longitude = st.number_input("Dropoff Longitude", value=-73.985428)
dropoff_latitude = st.number_input("Dropoff Latitude", value=40.748817)
passenger_count = st.number_input("Passenger Count", value=2)


url = 'https://taxifare-782621711539.europe-west1.run.app/predict'


params = {
    "pickup_datetime": f"{date} {time}",
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count
}


response = requests.get(url, params=params)

prediction = response.json()['fare']

## Finally, we can display the prediction to the user

st.markdown(f"## The predicted fare is: {round(prediction, 2)} $")
