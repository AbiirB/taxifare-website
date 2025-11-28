import streamlit as st
import requests
from datetime import datetime, time, date

# MY DRAFT
# location format : https://nominatim.openstreetmap.org/ui/search.html?q=1+quai+sainte+croix
# https://nominatim.openstreetmap.org/search?q=22+West+50th+Street%2C+New+York%2C+10022&format=jsonv2
# output needed from json = centroid":{"type": "Point","coordinates": [-0.5618156, 44.8330383]}


#  API URLS
url = 'https://taxifare-782621711539.europe-west1.run.app/predict'
geocode_api = 'https://nominatim.openstreetmap.org/ui/search'

# GEOCODING FUNCTION
def geocode(address: str):
    if not address:
        return None, None

    params = {
        "q": address,
        "format": "jsonv2",
        "limit": 1,
    }
    headers = {
        # Use a proper, identifying User-Agent as required by Nominatim
        "User-Agent": "taxifare-streamlit-app/1.0 (youremail@example.com)"
    }

    try:
        resp = requests.get(geocode_api, params=params, headers=headers, timeout=10)
        resp.raise_for_status()  # raises HTTPError for 4xx/5xx
        data = resp.json()

        if not data:
            st.warning(f"No geocoding result for: {address}")
            return None, None

        lon = float(data[0]["lon"])
        lat = float(data[0]["lat"])
        return lon, lat

    except requests.exceptions.RequestException as e:
        # This catches ConnectionError, Timeout, HTTPError, etc.
        st.error(f"Could not contact geocoding service: {e}")
        return None, None



#  PAGE CONFIG / UI
st.set_page_config(
    page_title="Taxi Fare Estimator",
    page_icon="🚕",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.title("Taxi Fare Estimator 🚕")
st.caption("Explore how trip details impact the taxi fare.")
st.markdown('<div class="stCard">', unsafe_allow_html=True)

st.markdown("### Enter the ride details:")

pickup_date = st.date_input("When do you want to ride?", value=datetime.now().date())
pickup_time = st.time_input("Pickup Time")
passenger_count = st.number_input("Passenger Count", value=2)

st.markdown("#### Locations")

pickup_location = st.text_input(
    "Where do we pick you up?",
    value="226 East 54th Street, New York, 10022",
)
dropoff_location = st.text_input(
    "Where to?",
    value="22 West 50th Street, New York, 10022",
)

# if pickup_location:
#     lon, lat = geocode(pickup_location)
#     if lon is None:
#         st.warning("Could not find pickup location.")
#     else:
#         st.session_state["pickup_longitude"] = lon
#         st.session_state["pickup_latitude"] = lat

# dropoff_location = st.text_input("Where to?", value="22 West 50th Street, New York, 10022")
# if dropoff_location:
#     lon, lat = geocode(dropoff_location)
#     if lon is None:
#         st.warning("Could not find dropoff location.")
#     else:
#         st.session_state["pickup_longitude"] = lon
#         st.session_state["pickup_latitude"] = lat


# MY API INPUTS
pickup_longitude = geocode(pickup_location[0])
pickup_latitude = geocode(pickup_location[1])
dropoff_longitude = geocode(dropoff_location[0])
dropoff_latitude = geocode(dropoff_location[1])


## PREDICTION OUTPUT
if st.button("🚕 Predict fare"):
    params = {
    "pickup_datetime": f"{pickup_date} {pickup_time}",
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count}

    with st.spinner("Contacting fare prediction API..."):
            response = requests.get(url, params=params)
            response.raise_for_status()
            prediction = response.json()['fare']

    st.markdown(f"## The predicted fare is: {round(prediction, 2)} $")
