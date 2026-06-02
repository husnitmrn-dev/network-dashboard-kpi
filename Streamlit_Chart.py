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
# CUSTOM CSS
# =====================================
st.markdown("""
<style>

/* Main Layout */
.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
}

/* Chart Card */
.chart-card{
    border:1px solid #2A2E39;
    border-radius:14px;
    padding:10px;
    background-color:#161A28;
    box-shadow:0px 2px 8px rgba(0,0,0,0.3);
    margin-bottom:15px;
}

/* KPI Card */
[data-testid="stMetric"]{
    border:1px solid #2A2E39;
    border-radius:12px;
    padding:15px;
    background-color:#161A28;
    box-shadow:0px 2px 8px rgba(0,0,0,0.3);
}

/* Sidebar */
[data-testid="stSidebar"]{
    border-right:1px solid #2A2E39;
}

/* Mobile */
@media (max-width:768px){

h1{
    font-size:26px !important;
}

[data-testid="stMetric"]{
    padding:8px !important;
}

.chart-card{
    padding:5px !important;
}

}

</style>
""", unsafe_allow_html=True)

# =====================================
# TITLE
# =====================================
st.markdown("""
<h1 style='text-align:center;'>
📡 Network KPI Dashboard
</h1>

<p style='text-align:center;color:gray;'>
Ericsson LTE KPI Monitoring
</p>
""", unsafe_allow_html=True)

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

    df["Datetime"] = (
        df["DATE_ID"]
        +
        pd.to_timedelta(
            df["hour_ID"],
            unit="h"
        )
    )

    return df

df = load_data()

# =====================================
# SIDEBAR FILTER
# =====================================
st.sidebar.header("Filter")

# Mobile View
is_mobile = st.sidebar.checkbox(
    "📱 Mobile View",
    value=False
)

# Site Filter
site_list = sorted(
    df["SITE_ID"]
    .dropna()
    .unique()
)

selected_site = st.sidebar.multiselect(
    "Site ID",
    site_list,
    default=[site_list[0]]
)

# Cell Filter
cell_options = sorted(
    df.loc[
        df["SITE_ID"].isin(selected_site),
        "EUtranCellFDD"
    ]
    .dropna()
    .unique()
)

selected_cells = st.sidebar.multiselect(
    "EUtranCellFDD",
    cell_options,
    default=cell_options
)

# Date Filter
min_date = df["DATE_ID"].min().date()
max_date = df["DATE_ID"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date)
)

# =====================================
# FILTER DATA
# =====================================
filtered = df[
    (df["SITE_ID"].isin(selected_site))
    &
    (df["EUtranCellFDD"].isin(selected_cells))
]

if len(date_range) == 2:

    start_date, end_date = date_range

    filtered = filtered[
        (
            filtered["DATE_ID"].dt.date
            >= start_date
        )
        &
        (
            filtered["DATE_ID"].dt.date
            <= end_date
        )
    ]

filtered = filtered.sort_values(
    "Datetime"
)

# =====================================
# KPI SUMMARY
# =====================================
st.subheader("KPI Summary")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Avg PRB Util (%)",
        round(
            filtered["PRB_Util_DL_ALL"].mean(),
            2
        )
    )

with c2:
    st.metric(
        "Total Payload (GB)",
        round(
            filtered["Total_Payload_All"].sum()/1024,
            2
        )
    )

with c3:
    st.metric(
        "Avg DL TP (kbps)",
        round(
            filtered[
                "User_Downlink_Average_Throughput_kbps"
            ].mean(),
            2
        )
    )

with c4:
    st.metric(
        "Avg Active User",
        round(
            filtered["Active User"].mean(),
            2
        )
    )

# =====================================
# CHART FUNCTION
# =====================================
def create_chart(column_name, title):

    st.markdown(
        '<div class="chart-card">',
        unsafe_allow_html=True
    )

    fig = px.line(
        filtered,
        x="Datetime",
        y=column_name,
        color="EUtranCellFDD",
        title=title,
        template="plotly_dark"
    )

    fig.update_layout(
        height=350,
        plot_bgcolor="#161A28",
        paper_bgcolor="#161A28",
        font=dict(color="white"),
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        ),
        legend_title_text="Cell"
    )

    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.1)"
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.1)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
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
# RAW DATA
# =====================================
st.subheader("Raw Data")

st.dataframe(
    filtered,
    use_container_width=True
)