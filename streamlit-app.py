import streamlit as st
import altair as alt
import pandas as pd

@st.cache
def get_data():
    df =  pd.read_pickle("data-streamlit/inflation_bps.pkl")
    return df.melt(id_vars=["date", "bulan", "tahun"])

df = get_data()
# st.dataframe(df)

st.title("Tingkat Inflasi Indonesia")

first_date = df["date"].min()
last_date = df["date"].max()

start_date = st.sidebar.date_input("Tanggal mulai", first_date)
end_date = st.sidebar.date_input('Tanggal akhir', last_date)
st.sidebar.caption("Hanya perhatikan bulan dan tahun, tanggal (1-31) dipilih bebas")

if start_date < end_date:
    st.sidebar.success(f"Start date: {start_date} \n\nEnd date: {end_date}")
else:
    st.sidebar.error('Error: End date must fall after start date.')

calculation_type=st.multiselect(
    "Silakan pilih bagaimana inflasi dihitung:",
    ["Year on Year", "Month to Month", "Year to date"],
    ["Year on Year"]
)

calculation_type_map = {
    "Year on Year": "yoy",
    "Month to Month": "mtm",
    "Year to date": "ytd"
}

st.write(type(start_date))
st.write(type(end_date))

selected_df = df[df["variable"].isin([calculation_type_map[ct] for ct in calculation_type])]
mask_date = (df["date"] >= start_date) & (df["date"] <= end_date)
selected_df = selected_df[mask_date]
# st.dataframe(selected_df)

color_range = ["#1f77b4", "#ff7f0e", "#2ca02c"]
# domain = [calculation_type_map[ct] for ct in calculation_type]

# date_scale = [start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")]

inflation_chart = alt.Chart(selected_df).mark_line().encode(
    x=alt.X("date:T", title="Periode"), # scale=alt.Scale(domain=date_scale)
    y=alt.Y("value:Q", title="Tingkat Inlfasi (%)"),
    color=alt.Color(
        "variable:O", 
        scale=alt.Scale(range=color_range),
        sort=["yoy", "mtm", "ytd"], 
        title="Perhitungan"),
    tooltip=[
        alt.Tooltip("date", title="Periode"),
        alt.Tooltip("variable", title="Perhitungan"),
        alt.Tooltip("value", title="Tingkat Inflasi (%)", format=".2f")
    ]
).properties(
    title="Tingkat Inflasi Indonesia"
).interactive()

st.altair_chart(inflation_chart, use_container_width=True)