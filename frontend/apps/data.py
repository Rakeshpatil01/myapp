import streamlit as st
import asyncio
from utils import consumer_airquality


def app():

    status = st.empty()
    connect = st.checkbox("Connect to WS Server")

    selected_visualizations = st.multiselect(
        "Select Visualizations", ["raw", "graph", "map"], default=["raw"]
    )

    columns = [col.empty() for col in st.columns(3)]

    window_size = st.number_input("Window Size", min_value=10, max_value=100)

    if connect:
        asyncio.run(
            consumer_airquality(
                dict(zip(selected_visualizations, columns)), window_size, status
            )
        )
    else:
        status.subheader(f"Disconnected.")
