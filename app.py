import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 Performans Analizi")

uploaded_file = st.file_uploader("Excel yükle", type=["xlsx"])

# Sabit bölümler (görünmesini istediğin tüm bölümler)
BOLUMLER = ["SEİRİM", "KESİM", "HAVLU", "PAKET", "KALİTE"]

# Excel parser (esnek ve güçlü)
def parse_excel(df_raw):
    data = []
    current_bolum = None

    for i in range(len(df_raw)):
        row = df_raw.iloc[i]
        col0 = str(row[0]).strip()

        # Bölüm yakala
        if "▶" in col0:
            current_bolum = col0.replace("▶", "").strip()

        # Operatör satırı
        elif current_bolum and col0 not in ["", "None", "nan"]:
            operator = col0

            numbers = []
            for val in row:
                try:
                    numbers.append(float(val))
                except:
                    continue

            if len(numbers) >= 2:
                calisilan = numbers[0]
                uretilen = numbers[1]

                data.append([current_bolum, operator, calisilan, uretilen])

    df = pd.DataFrame(data, columns=["Bölüm", "Operatör", "Çalışılan DK", "Üretilen DK"])
    return df

# =========================

if uploaded_file:
    try:
        df_raw = pd.read_excel(uploaded_file, header=None)
        df = parse_excel(df_raw)

        if not df.empty:
            df["Verimlilik"] = (df["Üretilen DK"] / df["Çalışılan DK"]) * 100

            # KPI
            st.subheader("📊 Genel Durum")

            col1, col2, col3 = st.columns(3)

            col1.metric("Toplam Çalışılan", int(df["Çalışılan DK"].sum()))
            col2.metric("Toplam Üretilen", int(df["Üretilen DK"].sum()))
            col3.metric("Ortalama Verim", f"%{df['Verimlilik'].mean():.1f}")

            # Grafik
            st.subheader("📊 Bölüm Performansı")

            bolum_ozet = df.groupby("Bölüm", as_index=False)["Verimlilik"].mean()

            fig = px.bar(
                bolum_ozet,
                x="Bölüm",
                y="Verimlilik",
                text_auto=".1f",
                color="Bölüm"
            )

            st.plotly_chart(fig, use_container_width=True)

        # =========================
        # RAPOR (HER ZAMAN GÖSTER)
        # =========================

        st.subheader("📄 Son Gün Performans Raporu")

        for bolum in BOLUMLER:
            st.write(f"### ▶ {bolum}")

            grup = df[df["Bölüm"] == bolum]

            if grup.empty:
                st.write("Boş")
            else:
                toplam_calisilan = grup["Çalışılan DK"].sum()
                toplam_uretilen = grup["Üretilen DK"].sum()
                verim = (toplam_uretilen / toplam_calisilan) * 100

                st.write(f"**Bölüm Verim: %{verim:.1f}**")

                for _, row in grup.iterrows():
                    st.write(
                        f"{row['Operatör']} | "
                        f"{row['Çalışılan DK']} dk | "
                        f"{row['Üretilen DK']} dk | "
                        f"%{row['Verimlilik']:.1f}"
                    )

            st.write("---")

    except Exception as e:
        st.error(f"Hata: {e}")
