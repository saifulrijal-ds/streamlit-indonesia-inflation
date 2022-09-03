import streamlit as st
import altair as alt
import pandas as pd

@st.cache
def get_data():
    df =  pd.read_pickle("data-streamlit/inflation_bps.pkl")
    return df.melt(id_vars=["date", "bulan", "tahun"])

df = get_data()
st.dataframe(df)

calculation_type=st.multiselect(
    "Silakan pilih bagaimana inflasi dihitung",
    ["Year on Year", "Month to Month", "Year to date"],
    ["Year on Year"]
)

calculation_type_map = {
    "Year on Year": "yoy",
    "Month to Month": "mtm",
    "Year to date": "ytd"
}

