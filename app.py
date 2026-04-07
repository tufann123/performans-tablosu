import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.markdown("""
<h1 style='text-align:center; color:white; background:#1f4e79; padding:10px;'>
SON GÜN OPERATÖR PERFORMANS TABLOSU
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
        df = df[[
            "Tarih",
            "Serim Operatörü",
            "Çalışılan Dakika",
            "Üretilen Dakika",
            "Verimlilik"
        ]]

        df = df.dropna(subset=["Serim Operatörü"])

        bolum = "SEİRİM"
        toplam_verim = df["Verimlilik"].mean()

        st.markdown(f"""
        <div style='background:#2f6690;color:white;padding:8px;margin-top:20px'>
        ▶ {bolum} - %{toplam_verim:.1f}
        </div>
        """, unsafe_allow_html=True)

        for _, row in df.iterrows():

            renk = get_color(row["Verimlilik"])

            html = f"""
            <div style='display:flex;justify-content:space-between;
                        padding:8px;border-bottom:1px solid #ddd'>

                <div style='width:30%'>{row['Serim Operatörü']}</div>
                <div style='width:20%'>{row['Çalışılan Dakika']}</div>
                <div style='width:20%'>{row['Üretilen Dakika']}</div>
                <div style='width:20%;background:{renk};text-align:center'>
                    %{row['Verimlilik']:.1f}
                </div>

            </div>
            """

            st.markdown(html, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Hata: {e}")
