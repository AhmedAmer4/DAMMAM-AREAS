
import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

st.set_page_config(layout="wide")
st.markdown("<h1 style='text-align: center; color: #3498db;'>GIZA ARABIA</h1>", unsafe_allow_html=True)

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
    "PENDING": "dodgerblue",
}

selected_layer = st.selectbox("اختر البند:", list(layer_files.keys()), index=0)

file_path = layer_files[selected_layer]

try:
    with open(file_path, encoding="utf-8") as f:
        gj = json.load(f)
    gdf = pd.json_normalize(gj["features"])
    gdf["geometry"] = gdf["geometry"]
    gdf["status"] = gdf["properties.PROG"].fillna("No Status")
    gdf["name_en"] = gdf["properties.name_en"].fillna("Unknown")

    gdf["color"] = gdf["status"].map(status_colors).fillna("lightblue")
    gdf["id"] = gdf.index.astype(str)
    gj["features"] = [f for i, f in enumerate(gj["features"]) if f.get("geometry")]
    for i, f in enumerate(gj["features"]):
        f["id"] = str(i)

    fig = px.choropleth_mapbox(
        gdf,
        geojson=gj,
        locations="id",
        color="color",
        color_discrete_map="identity",
        mapbox_style="satellite-streets",
        center={"lat": 26.4207, "lon": 50.0888},
        zoom=10.3,
        opacity=0.8,
        hover_name="name_en",
        hover_data=["status"]
    )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, height=650)

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("🧭 مفتاح الألوان:"):
        for status, color in status_colors.items():
            st.markdown(f"<span style='color:{color};font-weight:bold'>⬤ {status}</span>", unsafe_allow_html=True)
        st.markdown(f"<span style='color:lightblue;font-weight:bold'>⬤ No Status</span>", unsafe_allow_html=True)
except Exception as e:
    st.error(f"حدث خطأ أثناء تحميل الطبقة: {e}")
