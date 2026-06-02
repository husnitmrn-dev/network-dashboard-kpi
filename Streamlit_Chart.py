import streamlit as st
import pandas as pd
import plotly.express as px
# =====================================
# MOBILE MODE
# =====================================
is_mobile = st.sidebar.checkbox(
    "📱 Mobile View",
    value=False
)

# =====================================
# KPI CHARTS
# =====================================
st.subheader("KPI Charts Trendline")

# ===== MOBILE =====
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

# ===== DESKTOP =====
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
# MOBILE CSS
# =====================================
st.markdown("""
<style>

@media (max-width: 768px){

h1{
    font-size: 26px !important;
}

[data-testid="stMetric"]{
    padding: 8px;
}

}

</style>
""", unsafe_allow_html=True)
