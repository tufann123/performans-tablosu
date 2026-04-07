import streamlit as st
import pandas as pd

st.title("📊 Günlük Performans Analizi")

uploaded_file = st.file_uploader("Excel yükle", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    gerekli_kolonlar = ["Tarih", "Bölüm", "Operatör", "Çalışılan DK", "Üretilen DK"]
    
    if not all(col in df.columns for col in gerekli_kolonlar):
        st.error("Excel formatı hatalı!")
    else:
        df["Verimlilik"] = (df["Üretilen DK"] / df["Çalışılan DK"]) * 100

        st.subheader("📄 SON GÜN PERFORMANS TABLOSU")

        # Tarih al
        tarih = df["Tarih"].iloc[0]
        st.write(f"**Tarih: {tarih}**")

        bolumler = df.groupby("Bölüm")

        for bolum, grup in bolumler:
            st.write(f"## ▶ {bolum}")

            toplam_calisilan = grup["Çalışılan DK"].sum()
            toplam_uretilen = grup["Üretilen DK"].sum()
            bolum_verim = (toplam_uretilen / toplam_calisilan) * 100

            st.write(f"**Bölüm Verimlilik: %{bolum_verim:.1f}**")

            for _, row in grup.iterrows():
                st.write(
                    f"   {row['Operatör']} | "
                    f"{row['Çalışılan DK']} dk | "
                    f"{row['Üretilen DK']} dk | "
                    f"%{row['Verimlilik']:.1f}"
                )

            st.write("---")
