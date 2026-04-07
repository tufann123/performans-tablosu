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
    if verim >= 80:
        return "#c6efce"
    elif verim >= 50:
        return "#ffeb9c"
    else:
        return "#f4cccc"

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    try:
        html = "<div style='width:100%;font-family:Arial'>"

        # 🔥 TÜM OPERATÖR KOLONLARINI OTOMATİK BUL
        operator_cols = [col for col in df.columns if "Operatör" in col]

        for col in operator_cols:

            bolum_adi = col.replace(" Operatörü", "").upper()

            grup = df[[col, "Çalışılan Dakika", "Üretilen Dakika", "Verimlilik"]].copy()
            grup = grup.dropna(subset=[col])

            if grup.empty:
                continue

            ort_verim = grup["Verimlilik"].mean()

            # 🔵 BÖLÜM BAŞLIĞI
            html += f"""
            <div style='background:#2f6690;color:white;padding:10px;margin-top:15px;font-weight:bold'>
            ▶ {bolum_adi} - %{ort_verim:.1f}
            </div>
            """

            # 🔽 SATIRLAR
            for _, row in grup.iterrows():
                renk = get_color(row["Verimlilik"])

                html += f"""
                <div style='display:flex;border-bottom:1px solid #ddd;padding:6px'>
                    <div style='width:30%'>{row[col]}</div>
                    <div style='width:20%'>{row['Çalışılan Dakika']}</div>
                    <div style='width:20%'>{row['Üretilen Dakika']}</div>
                    <div style='width:20%;background:{renk};text-align:center'>
                        %{row['Verimlilik']:.1f}
                    </div>
                </div>
                """

        html += "</div>"

        components.html(html, height=1000, scrolling=True)

    except Exception as e:
        st.error(f"Hata: {e}")
