import streamlit as st
import geopandas as gpd
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Dammam Dashboard", layout="wide")

# CSS لتنسيق العنوان والخلفية
st.markdown(
    """
    <style>
    .main {
        background-color: #0d1b2a;
        color: white;
        border-radius: 10px;
        padding: 20px;
    }
    .title {
        font-size: 36px;
        font-weight: bold;
        color: #2196f3;
        text-align: center;
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 24px;
        font-weight: normal;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }
    .legend-box {
        background-color: #1e293b;
        padding: 10px;
        border-radius: 8px;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="title">GIZA ARABIA</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">WORK PROGRESS</div>', unsafe_allow_html=True)
st.markdown('<div class="main">', unsafe_allow_html=True)

# تعريف الألوان الموحدة لكل الحالات
status_colors = {
    "DONE": "limegreen",
    "IN PROGRESS": "yellow",
    "PLANNED": "pink",
    "PENDING": "dodgerblue",
    "NO STATUS": "lightblue"
}

# تحميل البيانات
def load_data(file_path):
    try:
        gdf = gpd.read_file(file_path)
        return gdf
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

# رسم الخريطة
def plot_map(gdf, layer_name):
    if gdf is not None and "PROG" in gdf.columns and "name_en" in gdf.columns:
        gdf["status_label"] = gdf["PROG"].fillna("").astype(str).str.strip().str.upper()

        # تطبيع وتعديل أسماء الحالات
        gdf["status_label"] = gdf["status_label"].replace({
            "": "NO STATUS",
            "DONE": "DONE",
            "IN PROGRESS": "IN PROGRESS",
            "PLANNED": "PLANNED",
            "PENDING": "PENDING"
        })
        gdf["status_label"] = gdf["status_label"].where(gdf["status_label"].isin(status_colors.keys()), "NO STATUS")
        gdf["hover_text"] = "Area: " + gdf["name_en"] + "<br>Status: " + gdf["status_label"]

        fig = px.choropleth_mapbox
