import streamlit as st
import geopandas as gpd
import json
import plotly.express as px
import pandas as pd
from streamlit_option_menu import option_menu
from streamlit_folium import st_folium
import folium

st.set_page_config(layout="wide")

# الخلفية
st.markdown("""
    <style>
        .main {
            background-color: #0F1117;
            color: white;
        }
        .block-container {
            border: 3px solid #0a3d62;
            padding: 20px;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# اللوجو والعنوان
col1, col2 = st.columns([8, 1])
with col1:
    st.markdown("<h1 style='text-align: center; color: deepskyblue;'>GIZA ARABIA</h1>", unsafe_allow_html=True)
with col2:
    st.image("giza_arabia_logo.jpg", width=80)

# ألوان الحالات
status_colors = {
    "DONE": "limegreen",
    "IN PROGRESS": "yellow",
    "PLANNED": "pink",
    "Pending": "dodgerblue",
    "No Status": "lightblue"
}

# تحميل البيانات مع التحقق
@st.cache_data
def load_geojson(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            gj = json.load(file)
            features = [f for f in gj["features"] if f.get("geometry")]
            return gpd.GeoDataFrame.from_features(features)
    except Exception as e:
        st.error(f"فشل تحميل الملف: {path} بسبب: {e}")
        return None

files = {
    "DATA GATHERING": "DATA GATHERING.json",
    "HCNREPAIR": "HCNREPAIR.json",
    "LEAK": "LEAK.json",
    "MLREPAIR": "MLREPAIR.geojson",
    "VALVES": "VALVES.json"
}

# الواجهة الرئيسية
selected = option_menu(
    menu_title=None,
    options=list(files.keys()),
    orientation="vertical"
)

geo_df = load_geojson(files[selected])

if geo_df is not None:
    # اسم العمود
    name_field = "name_en"
    status_field = "PROG"

    geo_df[status_field] = geo_df[status_field].fillna("No Status")
    geo_df["color"] = geo_df[status_field].map(lambda x: status_colors.get(x, "lightblue"))

    # إعداد الخريطة
    m = folium.Map(location=[26.4207, 50.0888], zoom_start=12, tiles="Esri.WorldImagery")

    for _, row in geo_df.iterrows():
        tooltip = f"<b>Area:</b> {row.get(name_field, 'N/A')}<br><b>Status:</b> {row.get(status_field, 'No Status')}"
        folium.GeoJson(
            row["geometry"],
            style_function=lambda x, color=row["color"]: {"fillColor": color, "color": "black", "weight": 1, "fillOpacity": 0.6},
            tooltip=tooltip
        ).add_to(m)

    # عرض الخريطة
    st_data = st_folium(m, width=1400, height=600)

    # مفتاح الألوان
    with st.expander("🔎 مفتاح الألوان"):
        for status, color in status_colors.items():
            st.markdown(f"<span style='color:{color}'>●</span> {status}", unsafe_allow_html=True)
else:
    st.warning("⚠️ لا توجد بيانات متاحة للعرض.")
