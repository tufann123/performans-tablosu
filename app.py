import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 Performans Dashboard")

# SESSION STATE (hafıza)
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Tarih", "Bölüm", "Operatör", "Çalışılan DK", "Üretilen DK"]
    )

df = st.session_state.data

# FORM
st.subheader("➕ Yeni Kayıt")

col1, col2, col3 = st.columns(3)

with col1:
    tarih = st.date_input("Tarih")
    bolum = st.text_input("Bölüm")

with col2:
    operator = st.text_input("Operatör")
    calisilan = st.number_input("Çalışılan DK", min_value=0)

with col3:
    uretilen = st.number_input("Üretilen DK", min_value=0)

if st.button("Kaydet"):
    new_row = pd.DataFrame(
        [[tarih, bolum, operator, calisilan, uretilen]],
        columns=df.columns
    )
    st.session_state.data = pd.concat([df, new_row], ignore_index=True)
    st.success("Kayıt eklendi!")

df = st.session_state.data

# ANALİZ
if not df.empty:
    df["Verimlilik"] = (df["Üretilen DK"] / df["Çalışılan DK"]) * 100

    st.markdown("---")

    # KPI
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Toplam Çalışılan", int(df["Çalışılan DK"].sum()))
    col2.metric("Toplam Üretilen", int(df["Üretilen DK"].sum()))
    col3.metric("Ortalama Verim", f"%{df['Verimlilik'].mean():.1f}")
    col4.metric("Kayıt Sayısı", len(df))

    # Grafik
    st.subheader("📊 Bölüm Bazlı Verimlilik")
    bolum_ozet = df.groupby("Bölüm", as_index=False)["Verimlilik"].mean()
    fig = px.bar(bolum_ozet, x="Bölüm", y="Verimlilik", text_auto=".1f")
    st.plotly_chart(fig, use_container_width=True)

    # Tablo
    st.subheader("📋 Kayıtlar")
    st.dataframe(df, use_container_width=True)
