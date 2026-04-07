import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# ✅ BAŞLIK GÜNCELLENDİ
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

        # 🔥 TÜM BÖLÜMLER
        bolumler = [
            ("SEİRİM", "Serim Operatörü"),
            ("KESİM", "Kesim Operatörü"),
            ("HAVLU", "Havlu Operatörü"),
            ("TASNİF", "Tasnif Operatörü"),
            ("METO", "Meto Operatörü"),
            ("DANTEL", "Dantel Operatörü"),
            ("BASKI HAZIRLIK", "Baskı Operatörü"),
        ]

        for bolum_adi, kolon in bolumler:

            if kolon not in df.columns:
                continue

            grup = df[[kolon, "Çalışılan Dakika", "Üretilen Dakika", "Verimlilik"]].copy()
            grup = grup.dropna(subset=[kolon])

            if grup.empty:
                continue

            ort_verim = grup["Verimlilik"].mean()

            # 🔵 BÖLÜM BAŞLIĞI
            html += f"""
            <div style='background:#2f6690;color:white;padding:10px;margin-top:15px;font-weight:bold'>
            ▶ {bolum_adi} - %{ort_verim:.1f}
            </div>
            """

            # 🔽 OPERATÖRLER
            for _, row in grup.iterrows():
                renk = get_color(row["Verimlilik"])

                html += f"""
                <div style='display:flex;border-bottom:1px solid #ddd;padding:6px'>
                    <div style='width:30%'>{row[kolon]}</div>
                    <div style='width:20%'>{row['Çalışılan Dakika']}</div>
                    <div style='width:20%'>{row['Üretilen Dakika']}</div>
                    <div style='width:20%;background:{renk};text-align:center'>
                        %{row['Verimlilik']:.1f}
                    </div>
                </div>
                """

        html += "</div>"

        components.html(html, height=900, scrolling=True)

    except Exception as e:
        st.error(f"Hata: {e}")
