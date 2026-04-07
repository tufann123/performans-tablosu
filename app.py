import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

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

if uploaded_file:
    try:
        excel_file = pd.ExcelFile(uploaded_file)
        sheet_names = excel_file.sheet_names

        html = "<div style='width:100%;font-family:Arial'>"

        tum_data = []

        # 🔥 TÜM SHEETLER
        for sheet in sheet_names:

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

            grup = df[gerekli].copy()
            grup = grup.dropna(subset=[col])

            if grup.empty:
                continue

            grup["Bölüm"] = sheet
            tum_data.append(grup)

            ort_verim = grup["Verimlilik"].mean()

            # 🔵 BÖLÜM BAŞLIK
            html += f"""
            <div style='background:#2f6690;color:white;padding:10px;margin-top:15px;font-weight:bold'>
            ▶ {sheet.upper()} - %{ort_verim:.1f}
            </div>
            """

            # 📋 TABLO BAŞLIK
            html += """
            <div style='display:flex;font-weight:bold;background:#eaeaea;padding:6px;border-bottom:2px solid #999'>
                <div style='width:25%'>Operatör</div>
                <div style='width:15%'>Tarih</div>
                <div style='width:20%'>Çalışılan DK</div>
                <div style='width:20%'>Üretilen DK</div>
                <div style='width:20%'>Verimlilik (%)</div>
            </div>
            """

            # 🔽 SATIRLAR
            for _, row in grup.iterrows():
                renk = get_color(row["Verimlilik"])

                html += f"""
                <div style='display:flex;border-bottom:1px solid #ddd;padding:6px'>
                    <div style='width:25%'>{row[col]}</div>
                    <div style='width:15%'>{row['Tarih']}</div>
                    <div style='width:20%'>{row['Çalışılan Dakika']}</div>
                    <div style='width:20%'>{row['Üretilen Dakika']}</div>
                    <div style='width:20%;background:{renk};text-align:center'>
                        %{0 if pd.isna(row['Verimlilik']) else round(row['Verimlilik'],1)}
                    </div>
                </div>
                """

        html += "</div>"

        # 📊 RAPOR GÖSTER
        components.html(html, height=900, scrolling=True)

        # 🔥 TÜM DATA BİRLEŞTİR
        if tum_data:
            tum_df = pd.concat(tum_data)

            tum_df["Tarih"] = pd.to_datetime(tum_df["Tarih"], errors="coerce")

            # 📈 GRAFİK
            st.subheader("📈 Günlük Ortalama Verim")

            gunluk = tum_df.groupby("Tarih")["Verimlilik"].mean().reset_index()
            st.line_chart(gunluk.set_index("Tarih"))

            # 📅 TARİH SEÇİMİ
            st.subheader("📅 Günlük Detay")

            secilen_tarih = st.date_input("Tarih seç")

            filtre = tum_df[tum_df["Tarih"].dt.date == secilen_tarih]

            if filtre.empty:
                st.warning("Bu tarihte veri yok")
            else:
                st.dataframe(filtre, use_container_width=True)

    except Exception as e:
        st.error(f"Hata: {e}")
