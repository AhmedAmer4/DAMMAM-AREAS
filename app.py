
import streamlit as st
import geopandas as gpd
import plotly.express as px

st.set_page_config(page_title="Dammam Dashboard", layout="wide")
st.title("Dammam Dashboard")

# تعريف ألوان الحالات
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
    if gdf is not None and "PROG" in gdf.columns:
        gdf["prog_clean"] = gdf["PROG"].astype(str).str.lower().str.strip()
        gdf["color"] = gdf["prog_clean"].map(status_colors).fillna("lightblue")
        fig = px.choropleth_mapbox(
            gdf,
            geojson=gdf.geometry,
            locations=gdf.index,
            color=gdf["color"],
            hover_name="PROG",
            center={"lat": 26.43, "lon": 50.10},
            mapbox_style="carto-positron",
            zoom=10,
        )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        st.plotly_chart(fig, use_container_width=True)
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
