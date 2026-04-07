import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 Performans Analizi")

uploaded_file = st.file_uploader("Excel yükle", type=["xlsx"])

# Sabit bölümler
BOLUMLER = ["SEİRİM", "KESİM", "HAVLU", "PAKET", "KALİTE"]

# Basit ve güvenli parser
def parse_excel_safe(df_raw):
    data = []
    current_bolum = None

    for i in range(len(df_raw)):
        row = df_raw.iloc[i]

        # tüm satırı string yap
        text = " ".join([str(x) for x in row if str(x) != "nan"]).upper()

        # bölüm yakala
        for b in BOLUMLER:
            if b in text:
                current_bolum = b

        # operatör + sayı yakala
        if current_bolum:
            numbers = []
            operator = None

            for val in row:
                # sayı mı?
                try:
                    numbers.append(float(val))
                except:
                    # metin mi?
                    if isinstance(val, str) and "-" in val:
                        operator = val.strip()

            if operator and len(numbers) >= 2:
                data.append([current_bolum, operator, numbers[0], numbers[1]])

    df = pd.DataFrame(data, columns=["Bölüm", "Operatör", "Çalışılan DK", "Üretilen DK"])
    return df


if uploaded_file:
    try:
        df_raw = pd.read_excel(uploaded_file, header=None)

        st.subheader("📄 Excel Önizleme")
        st.dataframe(df_raw)

        df = parse_excel_safe(df_raw)

        if df.empty:
            st.warning("⚠️ Veri okunamadı, sadece rapor gösteriliyor")
        else:
            df["Verimlilik"] = (df["Üretilen DK"] / df["Çalışılan DK"]) * 100

            # KPI
            st.subheader("📊 Genel Durum")

            col1, col2, col3 = st.columns(3)

            col1.metric("Toplam Çalışılan", int(df["Çalışılan DK"].sum()))
            col2.metric("Toplam Üretilen", int(df["Üretilen DK"].sum()))
            col3.metric("Ortalama Verim", f"%{df['Verimlilik'].mean():.1f}")

            # Grafik
            st.subheader("📊 Bölüm Performansı")

            bolum = df.groupby("Bölüm", as_index=False)["Verimlilik"].mean()
            fig = px.bar(bolum, x="Bölüm", y="Verimlilik", text_auto=".1f")

            st.plotly_chart(fig, use_container_width=True)

            # tablo
            st.subheader("📋 Detay Veri")
            st.dataframe(df, use_container_width=True)

        # RAPOR HER ZAMAN
        st.subheader("📄 Son Gün Performans Raporu")

        for bolum in BOLUMLER:
            st.write(f"### ▶ {bolum}")

            if 'df' in locals() and not df.empty:
                grup = df[df["Bölüm"] == bolum]
            else:
                grup = pd.DataFrame()

            if grup.empty:
                st.write("Boş")
            else:
                toplam_calisilan = grup["Çalışılan DK"].sum()
                toplam_uretilen = grup["Üretilen DK"].sum()

                if toplam_calisilan > 0:
                    verim = (toplam_uretilen / toplam_calisilan) * 100
                else:
                    verim = 0

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
        st.error(f"❌ Hata oluştu: {e}")
