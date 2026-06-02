import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================
# PAGE CONFIG
# =====================================
st.set_page_config(
    page_title="Network KPI Dashboard",
    layout="wide"
)

# =====================================
# LOAD DATA
# =====================================
@st.cache_data
def load_data():
    df = pd.read_csv("KPI Hourly.csv")

    df["DATE_ID"] = pd.to_datetime(df["DATE_ID"])

    df["SITE_ID"] = (
        df["EUtranCellFDD"]
        .astype(str)
        .str[:6]
    )

    return df

df = load_data()

# =====================================
# SIDEBAR FILTER
# =====================================
st.sidebar.title("Filter")

# Site ID
site_list = sorted(
    df["SITE_ID"]
    .dropna()
    .unique()
)

selected_site = st.sidebar.multiselect(
    "Site ID",
    site_list,
    default=site_list
)

# Cell Filter
cell_list = sorted(
    df.loc[
        df["SITE_ID"].isin(selected_site),
        "EUtranCellFDD"
    ]
    .dropna()
    .unique()
)

selected_cell = st.sidebar.multiselect(
    "EUtranCellFDD",
    cell_list,
    default=cell_list
)

# Date Filter
date_range = st.sidebar.date_input(
    "Date Range",
    value=(
        df["DATE_ID"].min().date(),
        df["DATE_ID"].max().date()
    )
)

# Apply Filter
filtered_df = df[
    (df["SITE_ID"].isin(selected_site))
    &
    (df["EUtranCellFDD"].isin(selected_cell))
]

if len(date_range) == 2:
    start_date, end_date = date_range

    filtered_df = filtered_df[
        (filtered_df["DATE_ID"].dt.date >= start_date)
        &
        (filtered_df["DATE_ID"].dt.date <= end_date)
    ]

# =====================================
# MOBILE MODE
# =====================================
is_mobile = st.sidebar.checkbox(
    "📱 Mobile View",
    value=False
)

# =====================================
# DASHBOARD TITLE
# =====================================
st.title("📊 Network KPI Dashboard")

# =====================================
# SUMMARY
# =====================================
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Site Count",
        filtered_df["SITE_ID"].nunique()
    )

with col2:
    st.metric(
        "Cell Count",
        filtered_df["EUtranCellFDD"].nunique()
    )

with col3:
    st.metric(
        "Records",
        len(filtered_df)
    )

# =====================================
# CHART FUNCTION
# =====================================
def create_chart(column_name, title):

    if column_name not in filtered_df.columns:
        st.warning(f"Column '{column_name}' not found")
        return

    chart_df = (
        filtered_df
        .groupby("hour_ID")[column_name]
        .mean()
        .reset_index()
        .sort_values("hour_ID")
    )

    fig = px.line(
        chart_df,
        x="hour_ID",
        y=column_name,
        markers=True,
        title=title
    )

    fig.update_layout(
        height=400
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================
# KPI CHARTS
# =====================================
st.subheader("KPI Charts Trendline")

if is_mobile:

    create_chart(
        "Total_Payload_All",
        "Total Payload Trend"
    )

    create_chart(
        "PRB_Util_DL_ALL",
        "PRB Utilization Trend"
    )

    create_chart(
        "User_Downlink_Average_Throughput_kbps",
        "User DL Throughput"
    )

    create_chart(
        "Cell_Downlink_Average_Throughput_kbps",
        "Cell DL Throughput"
    )

    create_chart(
        "User_Uplink_Average_Throughput_kbps",
        "User UL Throughput"
    )

    create_chart(
        "RRC_Connected_User",
        "RRC Connected User"
    )

else:

    col1, col2 = st.columns(2)

    with col1:
        create_chart(
            "Total_Payload_All",
            "Total Payload Trend"
        )

    with col2:
        create_chart(
            "PRB_Util_DL_ALL",
            "PRB Utilization Trend"
        )

    col3, col4 = st.columns(2)

    with col3:
        create_chart(
            "User_Downlink_Average_Throughput_kbps",
            "User DL Throughput"
        )

    with col4:
        create_chart(
            "Cell_Downlink_Average_Throughput_kbps",
            "Cell DL Throughput"
        )

    col5, col6 = st.columns(2)

    with col5:
        create_chart(
            "User_Uplink_Average_Throughput_kbps",
            "User UL Throughput"
        )

    with col6:
        create_chart(
            "RRC_Connected_User",
            "RRC Connected User"
        )

# =====================================
# ACTIVE USER
# =====================================
st.subheader("Active User Trend")

create_chart(
    "Active User",
    "Active User Trend"
)

# =====================================
# CSS
# =====================================
st.markdown("""
<style>

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
}

@media (max-width:768px){

h1{
    font-size:26px !important;
}

}

</style>
""", unsafe_allow_html=True)