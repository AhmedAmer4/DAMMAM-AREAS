import streamlit as st
import geopandas as gpd
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import json

st.set_page_config(layout="wide")

# === HEADER ===
col1, col2 = st.columns([6, 1])
with col1:
    st.markdown("<h1 style='color:#228be6;'>GIZA ARABIA</h1>", unsafe_allow_html=True)
with col2:
    st.image("giza_arabia_logo.jpg", width=80)

# === LAYERS ===
st.sidebar.markdown("### اختر الطبقة:")
layer = st.sidebar.radio("", ["DATA GATHERING", "HCNREPAIR", "LEAK", "MLREPAIR", "VALVES"])

# === FILE PATH ===
layer_files = {
    "DATA GATHERING": "DATA GATHERING.json",
    "HCNREPAIR": "HCNREPAIR.json",
    "LEAK": "LEAK.json",
    "MLREPAIR": "MLREPAIR.geojson",
    "VALVES": "VALVES.json"
}

file_path = layer_files.get(layer)

# === STATUS COLORS ===
status_colors = {
    "DONE": "limegreen",
    "IN PROGRESS": "yellow",
    "PLANNED": "pink",
    "Pending": "dodgerblue",
    "No Status": "lightblue"
}

# === LOAD & PROCESS DATA ===
try:
    gdf = gpd.read_file(file_path)
    gdf = gdf.to_crs(epsg=4326)

    # clean and prepare
    gdf["PROG"] = gdf["PROG"].fillna("No Status")
    gdf["status_label"] = gdf["PROG"].apply(lambda x: x if x in status_colors else "No Status")
    gdf["color"] = gdf["status_label"].map(status_colors)

    # assign id for map matching
    gdf["id"] = gdf.index.astype(str)

    # plot map
    fig = px.choropleth_mapbox(
        gdf,
        geojson=json.loads(gdf.to_json()),
        locations="id",
        color="status_label",
        color_discrete_map=status_colors,
        hover_name="name_en",
        hover_data={"status_label": True, "color": False, "id": False},
        mapbox_style="satellite-streets",
        zoom=10,
        center={"lat": gdf.geometry.centroid.y.mean(), "lon": gdf.geometry.centroid.x.mean()},
        opacity=0.6,
        height=650
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # render
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📘 مفاتيح الألوان:"):
        for key, color in status_colors.items():
            st.markdown(f"<span style='color:{color}; font-size:18px'>●</span> <b>{key}</b>", unsafe_allow_html=True)

except Exception as e:
    st.error(f"حدث خطأ أثناء تحميل الطبقة: {e}")
