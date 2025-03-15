import streamlit as st
import pandas as pd
import os

# Path relatif ke file CSV
csv_path = "submission/dashboard/main_data.csv"

st.write(f"Mencari file di: {os.path.abspath(csv_path)}")

# Pastikan file tersedia sebelum membaca
if os.path.exists(csv_path):
    df_air_quality = pd.read_csv(csv_path)
else:
    st.error(f"File '{csv_path}' tidak ditemukan! Pastikan file tersedia.")
    st.stop()

# Konversi kolom 'year' ke datetime
df_air_quality["year"] = pd.to_datetime(df_air_quality["year"], format='%Y')

# Mengisi nilai NaN dengan rata-rata numerik
df_air_quality.fillna(df_air_quality.select_dtypes(include=['number']).mean(), inplace=True)

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
        st.bar_chart(city_temperature.set_index("City"))

        # Grafik Kota dengan Suhu Maksimum & Minimum Sepanjang Tahun
        st.subheader("Kota dengan Suhu Tertinggi & Terendah di Semua Tahun")

        city_max_temp = df_air_quality.groupby("City")["TEMP"].max().reset_index()
        city_max_temp = city_max_temp.sort_values(by="TEMP", ascending=False)

        city_min_temp = df_air_quality.groupby("City")["TEMP"].min().reset_index()
        city_min_temp = city_min_temp.sort_values(by="TEMP", ascending=True)

        hottest_city_all_years = city_max_temp.iloc[0]
        coldest_city_all_years = city_min_temp.iloc[0]

        col1, col2 = st.columns(2)
        with col1:
            st.metric(label="\U0001F321️ Kota Terpanas Sepanjang Tahun", 
                      value=hottest_city_all_years["City"], 
                      delta=f"{hottest_city_all_years['TEMP']:.2f}°C")
            st.subheader("Top 10 Kota dengan Suhu Tertinggi")
            st.bar_chart(city_max_temp.head(10).set_index("City"))
        with col2:
            st.metric(label="\u2744️ Kota Terdingin Sepanjang Tahun", 
                      value=coldest_city_all_years["City"], 
                      delta=f"{coldest_city_all_years['TEMP']:.2f}°C")
            st.subheader("Top 10 Kota dengan Suhu Terendah")
            st.bar_chart(city_min_temp.head(10).set_index("City"))
