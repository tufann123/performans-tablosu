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

def parse_excel(df_raw):
    data = []
    current_bolum = None
    current_tarih = ""

    for i in range(len(df_raw)):
        row = df_raw.iloc[i]

        text = " ".join([str(x) for x in row if str(x) != "nan"]).upper()

        # bölüm satırı
        if any(b in text for b in ["SEİRİM","KESİM","HAVLU","TASNİF","METO","DANTEL","BASKI"]):
            current_bolum = text.strip()

        # operatör satırı
        numbers = []
        operator = None

        for val in row:
            try:
                numbers.append(float(val))
            except:
                if isinstance(val, str) and "-" in val:
                    operator = val.strip()

        if operator and len(numbers) >= 2:
            cal = numbers[0]
            ure = numbers[1]
            verim = (ure / cal) * 100 if cal > 0 else 0

            data.append({
                "bolum": current_bolum,
                "operator": operator,
                "cal": cal,
                "ure": ure,
                "verim": verim
            })

    return data

if uploaded_file:
    df_raw = pd.read_excel(uploaded_file, header=None)
    data = parse_excel(df_raw)

    if not data:
        st.error("Veri okunamadı")
    else:
        df = pd.DataFrame(data)

        for bolum in df["bolum"].unique():
            grup = df[df["bolum"] == bolum]

            toplam_verim = (grup["ure"].sum() / grup["cal"].sum()) * 100

            st.markdown(f"""
            <div style='background:#2f6690;color:white;padding:8px;margin-top:20px'>
            ▶ {bolum} - %{toplam_verim:.1f}
            </div>
            """, unsafe_allow_html=True)

            for _, row in grup.iterrows():
                renk = get_color(row["verim"])

                st.markdown(f"""
                <div style='display:flex;justify-content:space-between;
                            padding:8px;border-bottom:1px solid #ddd'>

                    <div style='width:30%'>{row['operator']}</div>
                    <div style='width:20%'>{row['cal']}</div>
                    <div style='width:20%'>{row['ure']}</div>
                    <div style='width:20%;background:{renk};text-align:center'>
                        %{row['verim']:.1f}
                    </div>

                </div>
                """, unsafe_allow_html=True)
