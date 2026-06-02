import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Network KPI Dashboard", layout="wide")

st.title("Network KPI Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("KPI Hourly.csv")

df = load_data()

def create_chart(column_name, title):
    if column_name not in df.columns:
        st.error(f"Kolom {column_name} tidak ditemukan")
        return

    chart_df = (
        df.groupby("hour_ID")[column_name]
        .mean()
        .reset_index()
    )

    fig = px.line(
        chart_df,
        x="hour_ID",
        y=column_name,
        title=title,
        markers=True
    )

    st.plotly_chart(fig, use_container_width=True)

is_mobile = st.sidebar.checkbox(
    "📱 Mobile View",
    value=False
)

st.subheader("KPI Charts Trendline")

create_chart("Total_Payload_All", "Total Payload Trend")
create_chart("PRB_Util_DL_ALL", "PRB Utilization Trend")
create_chart("User_Downlink_Average_Throughput_kbps", "User DL Throughput")
create_chart("Cell_Downlink_Average_Throughput_kbps", "Cell DL Throughput")
create_chart("User_Uplink_Average_Throughput_kbps", "User UL Throughput")
create_chart("RRC_Connected_User", "RRC Connected User")

st.subheader("Active User Trend")
create_chart("Active User", "Active User Trend")