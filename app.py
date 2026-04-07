import streamlit as st
import pandas as pd

st.title("📊 Günlük Performans Analizi")

uploaded_file = st.file_uploader("Excel yükle", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Kolon kontrolü
    gerekli_kolonlar = ["Tarih", "Bölüm", "Operatör", "Çalışılan DK", "Üretilen DK"]
    
    if not all(col in df.columns for col in gerekli_kolonlar):
        st.error("Excel formatı hatalı!")
    else:
        df["Verimlilik"] = (df["Üretilen DK"] / df["Çalışılan DK"]) * 100

        st.subheader("📋 Ham Veri")
        st.dataframe(df)

        st.subheader("📊 Bölüm Bazlı Performans")

        bolum_grup = df.groupby("Bölüm")

        for bolum, grup in bolum_grup:
            st.write(f"### ▶ {bolum}")

            ortalama = grup["Verimlilik"].mean()

            for _, row in grup.iterrows():
                st.write(f"{row['Operatör']} → %{row['Verimlilik']:.1f}")

            st.write(f"**Bölüm Ortalama: %{ortalama:.1f}**")
            st.write("---")

        st.subheader("🏆 En İyi Operatör")
        en_iyi = df.loc[df["Verimlilik"].idxmax()]
        st.success(f"{en_iyi['Operatör']} → %{en_iyi['Verimlilik']:.1f}")

        st.subheader("⚠️ En Düşük Operatör")
        en_kotu = df.loc[df["Verimlilik"].idxmin()]
        st.error(f"{en_kotu['Operatör']} → %{en_kotu['Verimlilik']:.1f}")
