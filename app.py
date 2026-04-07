import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

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
        # 🔥 TÜM SHEETLERİ OKU
        excel_file = pd.ExcelFile(uploaded_file)
        sheet_names = excel_file.sheet_names

        html = "<div style='width:100%;font-family:Arial'>"

        for sheet in sheet_names:

            df = pd.read_excel(uploaded_file, sheet_name=sheet)

            # Operatör kolonu bul
            operator_cols = [col for col in df.columns if "Operatör" in str(col)]

            if not operator_cols:
                continue

            col = operator_cols[0]

            gerekli_kolonlar = [
                col,
                "Çalışılan Dakika",
                "Üretilen Dakika",
                "Verimlilik"
            ]

            if not all(c in df.columns for c in gerekli_kolonlar):
                continue

            grup = df[gerekli_kolonlar].copy()
            grup = grup.dropna(subset=[col])

            if grup.empty:
                continue

            ort_verim = grup["Verimlilik"].mean()

            # 🔵 SHEET = BÖLÜM
            html += f"""
            <div style='background:#2f6690;color:white;padding:10px;margin-top:15px;font-weight:bold'>
            ▶ {sheet.upper()} - %{ort_verim:.1f}
            </div>
            """

            for _, row in grup.iterrows():
                renk = get_color(row["Verimlilik"])

                html += f"""
                <div style='display:flex;border-bottom:1px solid #ddd;padding:6px'>
                    <div style='width:30%'>{row[col]}</div>
                    <div style='width:20%'>{row['Çalışılan Dakika']}</div>
                    <div style='width:20%'>{row['Üretilen Dakika']}</div>
                    <div style='width:20%;background:{renk};text-align:center'>
                        %{0 if pd.isna(row['Verimlilik']) else round(row['Verimlilik'],1)}
                    </div>
                </div>
                """

        html += "</div>"

        components.html(html, height=1200, scrolling=True)

    except Exception as e:
        st.error(f"Hata: {e}")
