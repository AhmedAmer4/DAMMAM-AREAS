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

# وضع عنوان رئيسي
st.markdown('<div class="title">GIZA ARABIA</div>', unsafe_allow_html=True)
st.markdown('<div class="main">', unsafe_allow_html=True)

# تعريف الألوان حسب الحالة
status_colors = {
    "done": "limegreen",
    "in progress": "yellow",
    "planned": "pink",
    "pending": "dodgerblue",
    "": "lightblue",
    None: "lightblue"
}

# تحميل البيانات
def load_data(file_path):
    try:
        gdf = gpd.read_file(file_path)
        return gdf
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {e}")
        return None

# رسم الخريطة
def plot_map(gdf, layer_name):
    if gdf is not None and "PROG" in gdf.columns and "name_en" in gdf.columns:
        gdf["prog_clean"] = gdf["PROG"].astype(str).str.lower().str.strip()
        gdf["color"] = gdf["prog_clean"].map(status_colors).fillna("lightblue")
        gdf["hover_text"] = "Area: " + gdf["name_en"] + "<br>Status: " + gdf["PROG"]
        
        fig = px.choropleth_mapbox(
            gdf,
            geojson=gdf.geometry,
            locations=gdf.index,
            color=gdf["color"],
            hover_name="hover_text",
            center={"lat": 26.43, "lon": 50.10},
            mapbox_style="carto-positron",
            zoom=10,
        )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)

        # مفتاح الألوان
        st.markdown('<div class="legend-box"><b>مفتاح الألوان:</b>', unsafe_allow_html=True)
        for status, color in status_colors.items():
            name = status.upper() if status else "No Status"
            st.markdown(f'<span style="color:{color}">⬤</span> {name}', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning("لا توجد بيانات صالحة في هذه الطبقة.")

# التبويبات
tabs = {
    "DATA GATHERING": "DATA GATHERING.json",
    "HCNREPAIR": "HCNREPAIR.json",
    "LEAK": "LEAK.json",
    "MLREPAIR": "MLREPAIR.geojson",
    "VALVES": "VALVES.json"
}

selected_tab = st.sidebar.radio("اختر البند:", list(tabs.keys()))
gdf = load_data(tabs[selected_tab])
plot_map(gdf, selected_tab)

st.markdown('</div>', unsafe_allow_html=True)
