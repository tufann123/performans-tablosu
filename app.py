import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("📊 Performans Dashboard")

uploaded_file = st.file_uploader("Excel yükle", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    gerekli_kolonlar = ["Tarih", "Bölüm", "Operatör", "Çalışılan DK", "Üretilen DK"]

    if not all(col in df.columns for col in gerekli_kolonlar):
        st.error("Excel formatı hatalı!")
    else:
        # Hesaplamalar
        df["Verimlilik"] = (df["Üretilen DK"] / df["Çalışılan DK"]) * 100

        # KPI ALANI
        toplam_calisilan = df["Çalışılan DK"].sum()
        toplam_uretilen = df["Üretilen DK"].sum()
        ort_verim = df["Verimlilik"].mean()
        en_iyi = df.loc[df["Verimlilik"].idxmax()]
        en_kotu = df.loc[df["Verimlilik"].idxmin()]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Toplam Çalışılan DK", f"{toplam_calisilan:,.0f}")
        col2.metric("Toplam Üretilen DK", f"{toplam_uretilen:,.0f}")
        col3.metric("Ortalama Verimlilik", f"%{ort_verim:.1f}")
        col4.metric("En İyi Operatör", f"{en_iyi['Operatör']} (%{en_iyi['Verimlilik']:.1f})")

        st.markdown("---")

        # 📊 BÖLÜM BAZLI GRAFİK
        st.subheader("📊 Bölüm Bazlı Verimlilik")

        bolum_ozet = df.groupby("Bölüm", as_index=False)["Verimlilik"].mean()
        fig1 = px.bar(bolum_ozet, x="Bölüm", y="Verimlilik", text_auto=".1f")

        st.plotly_chart(fig1, use_container_width=True)

        # 👤 OPERATÖR PERFORMANSI
        st.subheader("👤 Operatör Performansı")

        fig2 = px.bar(
            df.sort_values("Verimlilik", ascending=False),
            x="Operatör",
            y="Verimlilik",
            color="Bölüm",
            text_auto=".1f"
        )

        st.plotly_chart(fig2, use_container_width=True)

        # 📋 DETAY TABLO
        st.subheader("📋 Detay Veri")
        st.dataframe(df, use_container_width=True)

        st.markdown("---")

        # 📄 SENİN FORMATTA RAPOR
        st.subheader("📄 Son Gün Performans Raporu")

        tarih = df["Tarih"].iloc[0]
        st.write(f"**Tarih: {tarih}**")

        bolumler = df.groupby("Bölüm")

        for bolum, grup in bolumler:
            st.write(f"### ▶ {bolum}")

            toplam_calisilan = grup["Çalışılan DK"].sum()
            toplam_uretilen = grup["Üretilen DK"].sum()
            bolum_verim = (toplam_uretilen / toplam_calisilan) * 100

            st.write(f"**Bölüm Verimlilik: %{bolum_verim:.1f}**")

            for _, row in grup.iterrows():
                st.write(
                    f"{row['Operatör']} | "
                    f"{row['Çalışılan DK']} dk | "
                    f"{row['Üretilen DK']} dk | "
                    f"%{row['Verimlilik']:.1f}"
                )

            st.write("---")
