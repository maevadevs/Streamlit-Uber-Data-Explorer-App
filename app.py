# This is the main entry of the Streamlit app
# Run: streamlit run uber_app.py

# Import libraries
import streamlit as st
import pandas as pd
import numpy as np

# Add app title
st.title("Uber Pickups in NYC")

# Fetch some data
DATE_COLUMN = "date/time"
DATA_URL = ("https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz")

## CACHING
## *******

## This will load a lot of data
## We don't want to re-run this everytime the app runs
## We want to cache this data instead
## For that purpose, use @st.cache on the data loader function
@st.cache
def load_data(nrows):
  # Read data with pandas
  data = pd.read_csv(DATA_URL, nrows=nrows)
  # Convert to lowercase
  data.rename(lambda x: str(x).lower(), axis="columns", inplace=True)
  # Convert datetime to datetime format
  data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
  # Return the final pandas dataframe
  return data

## Whenever you have a long-running computation in your code, consider refactoring it so 
## you can use @st.cache(), if possible.

## Caching limitations
## *******************
## 1. Streamlit will only check for changes within the current working directory. 
##    If you upgrade a Python library, Streamlit’s cache will only notice this if 
##    that library is installed inside your working directory.
##
## 2. If your function is not deterministic (that is, its output depends on random numbers), 
##    or if it pulls data from an external time-varying source (for example, a live stock 
##    market ticker service) the cached value will be none-the-wiser.
##
## 3. Lastly, you should not mutate the output of a cached function since cached values are 
##    stored by reference (for performance reasons and to be able to support libraries such 
##    as TensorFlow). Note that, here, Streamlit is smart enough to detect these mutations 
##    and show a loud warning explaining how to fix the problem.

# Create a text element and let the reader know the data is loading.
#data_load_state = st.text('Loading data...')

# Load 10,000 rows of data into the dataframe.
data = load_data(10000)

# Notify the reader that the data was successfully loaded.
#data_load_state.text("Loading Done! (using st.cache)")

## SIDEBAR WIDGETS
## ***************

# For Raw Data Section
st.sidebar.subheader("Raw Data Settings")
show_raw_data_widget = st.sidebar.checkbox('Show raw data')

# For Map Section
st.sidebar.subheader("Map Settings")
map_hour_to_filter_widget = st.sidebar.slider('Hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h

## INTRO TEXT
## **********

"""
In this project, we create an interactive app for exploring a public Uber dataset for pickups and drop-offs in New York City. We will fetch and cache data, draw charts, plot information on a map, and use interactive widgets, like a slider, to filter results.
"""

## INSPECT RAW DATA
## ****************

"""
## Raw data
"""

if show_raw_data_widget:
  st.subheader('Uber pickups')
  st.dataframe(data)
else:
  """
  Raw data is currently hidden. Check *Show raw data* in the sidebar to display.
  """

## HISTOGRAM
## *********

"""
## Histogram: Uber's busiest hours are in New York City
"""

st.subheader('Number of pickups by hour')

hist_values = np.histogram(
  data[DATE_COLUMN].dt.hour, 
  bins=24,
  range=(0,24))[0]

st.bar_chart(hist_values)

## MAP
## ***

"""
## Map: Map of all pickups
"""

# Using a slider for dynamic filtering
filtered_data = data[data[DATE_COLUMN].dt.hour == map_hour_to_filter_widget]
st.subheader(f'Map of all pickups at {map_hour_to_filter_widget}:00')
st.map(filtered_data)

