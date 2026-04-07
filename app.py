import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 Performans Analizi")

uploaded_file = st.file_uploader("Excel yükle", type=["xlsx"])

def parse_karma_format(df_raw):
    data = []
    current_bolum = None

    for _, row in df_raw.iterrows():
        first_col = str(row[0])

        if "▶" in first_col:
            current_bolum = first_col.replace("▶", "").strip()

        elif "-" in first_col and current_bolum:
            operator = first_col.strip()
            calisilan = row[2]
            uretilen = row[3]

            if pd.notna(calisilan) and pd.notna(uretilen):
                data.append([current_bolum, operator, calisilan, uretilen])

    df = pd.DataFrame(data, columns=["Bölüm", "Operatör", "Çalışılan DK", "Üretilen DK"])
    return df

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)

        # Eğer düz format değilse parse et
        if "Bölüm" not in df.columns:
            df_raw = pd.read_excel(uploaded_file, header=None)
            df = parse_karma_format(df_raw)

        df["Verimlilik"] = (df["Üretilen DK"] / df["Çalışılan DK"]) * 100

        # KPI
        col1, col2, col3 = st.columns(3)

        col1.metric("Toplam Çalışılan", int(df["Çalışılan DK"].sum()))
        col2.metric("Toplam Üretilen", int(df["Üretilen DK"].sum()))
        col3.metric("Ortalama Verim", f"%{df['Verimlilik'].mean():.1f}")

        # Grafik
        st.subheader("📊 Bölüm Performansı")
        bolum = df.groupby("Bölüm", as_index=False)["Verimlilik"].mean()
        fig = px.bar(bolum, x="Bölüm", y="Verimlilik", text_auto=".1f")
        st.plotly_chart(fig, use_container_width=True)

        # Tablo
        st.subheader("📋 Detay")
        st.dataframe(df, use_container_width=True)

        # Senin formatta çıktı
        st.subheader("📄 Rapor")

        for bolum, grup in df.groupby("Bölüm"):
            st.write(f"### ▶ {bolum}")

            toplam_calisilan = grup["Çalışılan DK"].sum()
            toplam_uretilen = grup["Üretilen DK"].sum()
            verim = (toplam_uretilen / toplam_calisilan) * 100

            st.write(f"**Bölüm Verim: %{verim:.1f}**")

            for _, row in grup.iterrows():
                st.write(
                    f"{row['Operatör']} | "
                    f"{row['Çalışılan DK']} | "
                    f"{row['Üretilen DK']} | "
                    f"%{row['Verimlilik']:.1f}"
                )

            st.write("---")

    except Exception as e:
        st.error(f"Hata: {e}")
