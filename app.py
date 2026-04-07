import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide")
st.title("📊 Performans Takip Sistemi")

DATA_FILE = "data.csv"

# Eğer dosya yoksa oluştur
if not os.path.exists(DATA_FILE):
    df_init = pd.DataFrame(columns=["Tarih", "Bölüm", "Operatör", "Çalışılan DK", "Üretilen DK"])
    df_init.to_csv(DATA_FILE, index=False)

# Veri oku
df = pd.read_csv(DATA_FILE)

# FORM ALANI
st.subheader("➕ Yeni Kayıt Ekle")

with st.form("veri_form"):
    tarih = st.date_input("Tarih")
    bolum = st.text_input("Bölüm")
    operator = st.text_input("Operatör")
    calisilan = st.number_input("Çalışılan DK", min_value=0)
    uretilen = st.number_input("Üretilen DK", min_value=0)

    submit = st.form_submit_button("Kaydet")

    if submit:
        new_data = pd.DataFrame([[tarih, bolum, operator, calisilan, uretilen]],
                                columns=df.columns)

        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

        st.success("Kayıt eklendi!")

# ANALİZ
if not df.empty:
    df["Verimlilik"] = (df["Üretilen DK"] / df["Çalışılan DK"]) * 100

    st.subheader("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Toplam Çalışılan", int(df["Çalışılan DK"].sum()))
    col2.metric("Toplam Üretilen", int(df["Üretilen DK"].sum()))
    col3.metric("Ortalama Verim", f"%{df['Verimlilik'].mean():.1f}")

    st.subheader("📋 Tüm Kayıtlar")
    st.dataframe(df, use_container_width=True)
