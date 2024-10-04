import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set style seaborn
sns.set(style='dark')

# Menyiapkan data day_df yang sudah bersih
day_df = pd.read_csv("https://raw.githubusercontent.com/callmenidd/Proyek-analisis-data/refs/heads/main/dashboard/main_data.csv")
day_df.head()

# Mengubah nama judul kolom
day_df.rename(columns={
    'dteday': 'dateday',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)

# Membuat function untuk data frame

def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df

def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df   

def create_byseason_df(df):
    season_df = df.groupby(by='season').agg({
        "count": "sum"
    }).reset_index() 
    return season_df

def create_byweather_df(df):
    weather_df = df.groupby(by='weather_cond').agg({
        "count": "sum"
    }).reset_index() 
    return weather_df

def create_byworkingday_df(df):
    workingday_df = df.groupby(by='workingday').agg({
        "count": "sum"
    }).reset_index() 
    return workingday_df

# Membuat komponen filter
min_date = pd.to_datetime(day_df['dateday']).dt.date.min()
max_date = pd.to_datetime(day_df['dateday']).dt.date.max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image('https://github.com/callmenidd/Proyek-analisis-data/blob/main/dashboard/supercycle_logo.png?raw=true')

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df['dateday'] >= str(start_date)) & 
                (day_df['dateday'] <= str(end_date))]
   
# Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
season_df = create_byseason_df(main_df)
weather_df = create_byweather_df(main_df)
workingday_df = create_byworkingday_df(main_df)

# Membuat Dashboard

st.header('Supercycle Bike Rental Dashboard 🚵')  

# Statistik Pengguna Rental Per Hari
st.subheader('Daily Rentals')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Casual User', value= daily_rent_casual)

with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Registered User', value= daily_rent_registered)
 
with col3:
    daily_rent_total = daily_rent_df['count'].sum()
    st.metric('Total User', value= daily_rent_total)


# Membuah jumlah penyewaan berdasarkan kondisi musim
st.subheader('Rata-Rata Penyewaan Sepeda berdasarkan Musim')
fig, ax = plt.subplots()
sns.barplot(
    x='season',
    y='count',
    hue='season',
    data=season_df,
    palette='viridis'
)

for index, row in enumerate(season_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)
st.pyplot(fig)

# Membuah jumlah penyewaan berdasarkan kondisi cuaca
st.subheader('Rata-Rata Penyewaan Sepeda berdasarkan Cuaca')
fig, ax = plt.subplots()
sns.barplot(
    x='weather_cond',
    y='count',
    hue='weather_cond',
    data=weather_df,
    palette='viridis'
)

for index, row in enumerate(weather_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)
st.pyplot(fig)

# Berdasarkan workingday
st.subheader('Jumlah Penyewaan Sepeda berdasarkan Hari Kerja')
fig, ax = plt.subplots()
sns.barplot(
    x='workingday',
    y='count',
    data=workingday_df,
    palette='Set2',
    ax=ax)

for index, row in enumerate(workingday_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xticks([0,1],['Libur','Hari Kerja'])
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=10)
ax.tick_params(axis='y', labelsize=10)
st.pyplot(fig)


st.caption('Copyright (c) Nidya Aulia Adji Putri 2024')