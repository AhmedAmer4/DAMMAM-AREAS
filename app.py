
import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px
import json
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide", page_title="Dammam Dashboard")

st.markdown("<h1 style='text-align: center; color: #3399ff;'>GIZA ARABIA</h1>", unsafe_allow_html=True)

layer_files = {
    "DATA GATHERING": "DATA GATHERING.json",
    "HCNREPAIR": "HCNREPAIR.json",
    "LEAK": "LEAK.json",
    "MLREPAIR": "MLREPAIR.geojson",
    "VALVES": "VALVES.json"
}

status_colors = {
    "DONE": "limegreen",
    "IN PROGRESS": "yellow",
    "PLANNED": "pink",
    "Pending": "dodgerblue",
    None: "lightblue",
    "": "lightblue",
    "NO STATUS": "lightblue"
}

selected_layer = option_menu(
    menu_title="اختر البند:",
    options=list(layer_files.keys()),
    orientation="vertical"
)

if selected_layer:
    file_path = layer_files[selected_layer]
    if file_path.endswith(".geojson"):
        gdf = gpd.read_file(file_path)
    else:
        with open(file_path, encoding='utf-8') as f:
            gj = json.load(f)
        gdf = gpd.GeoDataFrame.from_features(gj["features"])

    status_col = None
    for col in gdf.columns:
        if col.upper() in ["PROG", "STATUS", "STAT", "PROGRESS"]:
            status_col = col
            break

    if status_col:
        gdf["status_label"] = gdf[status_col].fillna("NO STATUS").astype(str)
    else:
        gdf["status_label"] = "NO STATUS"

    gdf["color"] = gdf["status_label"].map(status_colors).fillna("lightblue")

    fig = px.choropleth_mapbox(
        geojson=gdf.geometry.__geo_interface__,
        locations=gdf.index,
        color=gdf["status_label"],
        mapbox_style="satellite",
        center={"lat": 26.43, "lon": 50.1},
        zoom=10,
        opacity=0.5,
        color_discrete_map=status_colors,
        hover_name=gdf.get("name_en", gdf.index),
        hover_data={"status_label": True}
    )

    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=700)

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("🧭 مفتاح الألوان:"):
        for label, color in status_colors.items():
            if label:
                st.markdown(f"<span style='color:{color}'>●</span> {label}", unsafe_allow_html=True)
