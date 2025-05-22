import streamlit as st
import pandas as pd
from weather_fetcher import hourly_dataframe  # make sure it's accessible

st.title("📊 Weather Monitoring Dashboard")

st.line_chart(hourly_dataframe.set_index("date")[["temperature_2m", "relative_humidity_2m"]])
st.bar_chart(hourly_dataframe.set_index("date")[["rain"]])

st.write("### Raw Data")
st.dataframe(hourly_dataframe)
