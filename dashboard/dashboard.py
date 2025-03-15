import streamlit as st
import pandas as pd
import plotly.express as px

df_air_quality = pd.read_csv(r"C:\Users\muham\Documents\Dicoding\AnalisisData\submission\dashboard\main_data.csv")

df_air_quality["year"] = pd.to_datetime(df_air_quality["year"], format='%Y')

df_air_quality.fillna(df_air_quality.select_dtypes(include=['number']).mean(numeric_only=True), inplace=True)

st.set_page_config(
    page_title="Dashboard Suhu Kota",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Flag_of_the_People%27s_Republic_of_China.svg/200px-Flag_of_the_People%27s_Republic_of_China.svg.png",
                  use_column_width=True)

st.sidebar.title("\U0001F3D9️ Navigasi")
page = st.sidebar.radio("Pilih Halaman", ["\U0001F4CA Data", "\U0001F4C8 Visualisasi"])

st.sidebar.subheader("Filter Tahun")
selected_year = st.sidebar.selectbox("Pilih Tahun", df_air_quality["year"].dt.year.unique())
df_filtered = df_air_quality[df_air_quality["year"].dt.year == selected_year]

city_temperature = df_filtered.groupby("City")["TEMP"].mean().reset_index()
city_temperature = city_temperature.sort_values(by="TEMP", ascending=False)

st.title("\U0001F30D Dashboard Suhu Rata-rata Kota di Negara China (2013-2017)")
st.markdown("---")

if not city_temperature.empty:
    hottest_city = city_temperature.iloc[0]
    coldest_city = city_temperature.iloc[-1]

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="\U0001F321️ Kota Terpanas", 
                  value=hottest_city["City"], 
                  delta=f"{hottest_city['TEMP']:.2f}°C")
    with col2:
        st.metric(label="\u2744️ Kota Terdingin", 
                  value=coldest_city["City"], 
                  delta=f"{coldest_city['TEMP']:.2f}°C")

    st.markdown("---")

    if page == "\U0001F4CA Data":
        st.subheader("Data Suhu Rata-rata Tiap Kota")
        st.dataframe(city_temperature.style.format({"TEMP": "{:.2f}°C"}))
    
    elif page == "\U0001F4C8 Visualisasi":
        st.subheader("Grafik Suhu Rata-rata per Kota")
        fig = px.bar(city_temperature, x="TEMP", y="City", 
                     title=f"Urutan Kota dengan Suhu Rata-rata ({selected_year})",
                     labels={"TEMP": "Suhu Rata-rata (°C)", "City": "Kota"},
                     color="TEMP", color_continuous_scale="Blues",
                     orientation="h")
        st.plotly_chart(fig, use_container_width=True)
        
        # **Visualization: Hottest & Coldest Cities Across All Years**
        st.subheader("Kota dengan Suhu Tertinggi & Terendah di Semua Tahun")

        city_max_temp = df_air_quality.groupby("City")["TEMP"].max().reset_index()
        city_max_temp = city_max_temp.sort_values(by="TEMP", ascending=False).head(10)

        city_min_temp = df_air_quality.groupby("City")["TEMP"].min().reset_index()
        city_min_temp = city_min_temp.sort_values(by="TEMP", ascending=True).head(10)

        col1, col2 = st.columns(2)

        with col1:
            fig_max_temp = px.bar(city_max_temp, x="TEMP", y="City", 
                                  title="Top 10 Kota dengan Suhu Tertinggi Sepanjang Tahun",
                                  labels={"TEMP": "Suhu Maksimum (°C)", "City": "Kota"},
                                  color="TEMP", color_continuous_scale="Reds",
                                  orientation="h")
            fig_max_temp.update_yaxes(categoryorder="total ascending")
            st.plotly_chart(fig_max_temp, use_container_width=True)

        with col2:
            fig_min_temp = px.bar(city_min_temp, x="TEMP", y="City", 
                                  title="Top 10 Kota dengan Suhu Terendah Sepanjang Tahun",
                                  labels={"TEMP": "Suhu Minimum (°C)", "City": "Kota"},
                                  color="TEMP", color_continuous_scale="Blues",
                                  orientation="h")
            fig_min_temp.update_yaxes(categoryorder="total descending")
            st.plotly_chart(fig_min_temp, use_container_width=True)
            fig_min_temp.update_yaxes(categoryorder="total descending")
            st.plotly_chart(fig_min_temp, use_container_width=True)
