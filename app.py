import streamlit as st
import geopandas as gpd
import plotly.express as px
from streamlit_option_menu import option_menu

st.set_page_config(layout="wide")

# ---------- HEADER -------------
col1, col2 = st.columns([10, 1])
with col1:
    st.markdown("<h1 style='color:#3399ff;'>GIZA ARABIA</h1>", unsafe_allow_html=True)
with col2:
    st.image("logo_giza.png", width=80)

st.markdown("---")

# ---------- LOAD DATA -----------
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
    "NO STATUS": "lightblue"
}

# ---------- SIDEBAR -------------
st.sidebar.markdown("اختر الطبقة:")
selected_layer = st.sidebar.radio("", list(layer_files.keys()))

# ---------- LOAD AND CLEAN GEOJSON -----------
@st.cache_data

def load_data(file):
    gdf = gpd.read_file(file)
    gdf["PROG"] = gdf["PROG"].fillna("NO STATUS")
    gdf["color"] = gdf["PROG"].apply(lambda x: status_colors.get(x.upper(), "lightblue"))
    return gdf

gdf = load_data(layer_files[selected_layer])

# ---------- PLOT MAP -------------
fig = px.choropleth_mapbox(
    gdf,
    geojson=gdf.geometry,
    locations=gdf.index,
    color=gdf["color"],
    hover_name="name_en",
    hover_data={"PROG": True, "color": False, "index": False},
    mapbox_style="satellite-streets",
    zoom=10,
    center={"lat": gdf.geometry.centroid.y.mean(), "lon": gdf.geometry.centroid.x.mean()},
    opacity=0.6
)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

st.plotly_chart(fig, use_container_width=True)

# ---------- LEGEND -------------
with st.expander("🗺️ مفاتيح الألوان:"):
    for status, color in status_colors.items():
        st.markdown(f"<span style='color:{color}; font-size:18px;'>⬤</span> {status}", unsafe_allow_html=True)
