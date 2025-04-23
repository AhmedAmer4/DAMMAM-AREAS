
import streamlit as st
import geopandas as gpd
import json
import plotly.express as px
import pandas as pd

# إعداد الصفحة
st.set_page_config(layout="wide", page_title="GIZA ARABIA Dashboard")

# --- ترويسة مع اللوجو ---
col1, col2 = st.columns([8, 1])
with col1:
    st.markdown("<h1 style='color:#1f77b4;'>GIZA ARABIA</h1>", unsafe_allow_html=True)
with col2:
    st.image("logo_giza.png", use_column_width=True)

# --- تحميل الملفات ---
layers = {
    "DATA GATHERING": "DATA GATHERING.json",
    "HCNREPAIR": "HCNREPAIR.json",
    "LEAK": "LEAK.json",
    "MLREPAIR": "MLREPAIR.geojson",
    "VALVES": "VALVES.json"
}
selected_layer = st.sidebar.radio("اختر البند:", list(layers.keys()))

# تحميل الطبقة المختارة
if layers[selected_layer].endswith(".geojson"):
    gdf = gpd.read_file(layers[selected_layer])
else:
    with open(layers[selected_layer], encoding="utf-8") as f:
        gj = json.load(f)
    gdf = gpd.GeoDataFrame.from_features(gj["features"])

# --- إعداد الألوان حسب الحالة ---
status_colors = {
    "DONE": "limegreen",
    "IN PROGRESS": "yellow",
    "PENDING": "dodgerblue",
    "PLANNED": "pink",
    "NO STATUS": "lightblue"
}

if "prog" in gdf.columns:
    gdf["prog"] = gdf["prog"].fillna("NO STATUS")
else:
    gdf["prog"] = "NO STATUS"

gdf["color"] = gdf["prog"].map(lambda x: status_colors.get(x.upper(), "lightblue"))

# --- خريطة ---
fig = px.choropleth_mapbox(
    gdf,
    geojson=gdf.geometry,
    locations=gdf.index,
    color=gdf["color"],
    color_discrete_map="identity",
    hover_name="prog",
    hover_data={"color": False, "prog": True, "name_en": True},
    center={"lat": 26.43, "lon": 50.1},
    zoom=10,
    height=650
)
fig.update_layout(mapbox_style="satellite-streets", margin={"r":0,"t":0,"l":0,"b":0})

# --- عرض الخريطة ---
st.plotly_chart(fig, use_container_width=True)

# --- مفتاح الألوان ---
st.markdown("### 🗺️ مفاتيح الألوان:")
for label, color in status_colors.items():
    st.markdown(f"<span style='color:{color};font-size:20px;'>●</span> **{label}**", unsafe_allow_html=True)
