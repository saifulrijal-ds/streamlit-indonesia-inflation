import streamlit as st
import altair as alt
import pandas as pd

@st.cache
def get_data():
    return pd.read_pickle("data-streamlit/inflation_bps.pkl")

df = get_data()
st.dataframe(df)