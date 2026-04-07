import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from io import BytesIO

st.set_page_config(layout="wide")

# 🔵 BAŞLIK
st.markdown("""
<h1 style='text-align:center; color:white; background:#1f4e79; padding:10px;'>
OPERATÖR PERFORMANS TABLOSU
</h1>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Excel yükle", type=["xlsx"])

def get_color(verim):
    if pd.isna(verim):
        return "#eeeeee"
    elif verim >= 80:
        return "#c6efce"
    elif verim >= 50:
        return "#ffeb9c"
    else:
        return "#f4cccc"

# 📥 Excel export fonksiyonu
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Rapor')
    return output.getvalue()

if uploaded_file:
    try:
        excel_file = pd.ExcelFile(uploaded_file)
        tum_data = []

        # 🔥 TÜM SHEETLERİ OKU
        for sheet in excel_file.sheet_names:
            df = pd.read_excel(uploaded_file, sheet_name=sheet)

            operator_cols = [col for col in df.columns if "Operatör" in str(col)]
            if not operator_cols:
                continue

            col = operator_cols[0]

            gerekli = [
                "Tarih",
                col,
                "Çalışılan Dakika",
                "Üretilen Dakika",
                "Verimlilik"
            ]

            if not all(c in df.columns for c in gerekli):
                continue

            temp = df[gerekli].copy()
            temp = temp.dropna(subset=[col])
            temp["Bölüm"] = sheet

            tum_data.append(temp)

        if not tum_data:
            st.warning("Veri bulunamadı")
            st.stop()

        tum_df = pd.concat(tum_data)
        tum_df["Tarih"] = pd.to_datetime(tum_df["Tarih"], errors="coerce")

        # 📅 TARİH SEÇ
        tarihler = tum_df["Tarih"].dropna().dt.date.unique()
        tarihler = sorted(tarihler)

        secilen_tarih = st.selectbox("📅 Tarih seç", tarihler)

        # 🔥 FİLTRE
        filtre_df = tum_df[tum_df["Tarih"].dt.date == secilen_tarih]

        # 📥 EXCEL İNDİR
        excel_data = to_excel(filtre_df)

        st.download_button(
            label="📥 Excel olarak indir",
            data=excel_data,
            file_name=f"performans_{secilen_tarih}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        # 🔵 HTML RAPOR
        html = "<div style='width:100%;font-family:Arial'>"

        for bolum in filtre_df["Bölüm"].unique():

            grup = filtre_df[filtre_df["Bölüm"] == bolum]

            ort_verim = grup["Verimlilik"].mean()

            html += f"""
            <div style='background:#2f6690;color:white;padding:10px;margin-top:15px;font-weight:bold'>
            ▶ {bolum.upper()} - %{round(ort_verim,2)}
            </div>
            """

            html += """
            <div style='display:flex;font-weight:bold;background:#eaeaea;padding:6px;border-bottom:2px solid #999'>
                <div style='width:25%'>Operatör</div>
                <div style='width:15%'>Tarih</div>
                <div style='width:20%'>Çalışılan DK</div>
                <div style='width:20%'>Üretilen DK</div>
                <div style='width:20%'>Verimlilik (%)</div>
            </div>
            """

            for _, row in grup.iterrows():
                renk = get_color(row["Verimlilik"])

                tarih = ""
                if not pd.isna(row["Tarih"]):
                    tarih = pd.to_datetime(row["Tarih"]).strftime("%d.%m.%Y")

                calisilan = int(row["Çalışılan Dakika"]) if not pd.isna(row["Çalışılan Dakika"]) else ""
                uretilen = f"{row['Üretilen Dakika']:.1f}" if not pd.isna(row["Üretilen Dakika"]) else ""
                verim = f"{row['Verimlilik']:.2f}" if not pd.isna(row["Verimlilik"]) else "0.00"

                html += f"""
                <div style='display:flex;border-bottom:1px solid #ddd;padding:6px'>
                    <div style='width:25%'>{row['Bölüm'] if False else row.iloc[1]}</div>
                    <div style='width:15%'>{tarih}</div>
                    <div style='width:20%'>{calisilan}</div>
                    <div style='width:20%'>{uretilen}</div>
                    <div style='width:20%;background:{renk};text-align:center'>
                        %{verim}
                    </div>
                </div>
                """

        html += "</div>"

        components.html(html, height=900, scrolling=True)

        # 📈 GRAFİK
        st.subheader("📈 Günlük Ortalama Verim")
        gunluk = tum_df.groupby("Tarih")["Verimlilik"].mean().reset_index()
        st.line_chart(gunluk.set_index("Tarih"))

    except Exception as e:
        st.error(f"Hata: {e}")
