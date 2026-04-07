import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from io import BytesIO

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

def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

if uploaded_file:
    try:
        excel_file = pd.ExcelFile(uploaded_file)
        tum_data = []

        for sheet in excel_file.sheet_names:
            df = pd.read_excel(uploaded_file, sheet_name=sheet)

            operator_cols = [col for col in df.columns if "Operatör" in str(col)]
            if not operator_cols:
                continue

            col = operator_cols[0]

            gerekli = ["Tarih", col, "Çalışılan Dakika", "Üretilen Dakika", "Verimlilik"]

            if not all(c in df.columns for c in gerekli):
                continue

            temp = df[gerekli].copy()
            temp = temp.dropna(subset=[col])
            temp["Bölüm"] = sheet
            temp.rename(columns={col: "Operatör"}, inplace=True)

            tum_data.append(temp)

        if not tum_data:
            st.warning("Veri bulunamadı")
            st.stop()

        tum_df = pd.concat(tum_data)
        tum_df["Tarih"] = pd.to_datetime(tum_df["Tarih"], errors="coerce")

        # 📅 TARİH SEÇ
        tarihler = sorted(tum_df["Tarih"].dropna().dt.date.unique())
        secilen_tarih = st.selectbox("📅 Tarih seç", tarihler)

        filtre_df = tum_df[tum_df["Tarih"].dt.date == secilen_tarih]

        # 📥 EXCEL EXPORT
        st.download_button(
            "📥 Excel indir",
            data=to_excel(filtre_df),
            file_name=f"performans_{secilen_tarih}.xlsx"
        )

        # 📊 EN İYİ / EN KÖTÜ
        st.subheader("📊 Günün Özeti")

        col1, col2 = st.columns(2)

        if not filtre_df.empty:
            en_iyi = filtre_df.loc[filtre_df["Verimlilik"].idxmax()]
            en_kotu = filtre_df.loc[filtre_df["Verimlilik"].idxmin()]

            col1.success(f"🏆 En iyi: {en_iyi['Operatör']} (%{en_iyi['Verimlilik']:.2f})")
            col2.error(f"⚠️ En kötü: {en_kotu['Operatör']} (%{en_kotu['Verimlilik']:.2f})")

        # 🔵 HTML RAPOR
        html = "<div style='width:100%;font-family:Arial'>"

        for bolum in filtre_df["Bölüm"].unique():

            grup = filtre_df[filtre_df["Bölüm"] == bolum]
            ort = grup["Verimlilik"].mean()

            html += f"""
            <div style='background:#2f6690;color:white;padding:10px;margin-top:15px;font-weight:bold'>
            ▶ {bolum.upper()} - %{ort:.2f}
            </div>
            """

            html += """
            <div style='display:flex;font-weight:bold;background:#eaeaea;padding:6px'>
                <div style='width:25%'>Operatör</div>
                <div style='width:15%'>Tarih</div>
                <div style='width:20%'>Çalışılan DK</div>
                <div style='width:20%'>Üretilen DK</div>
                <div style='width:20%'>Verimlilik</div>
            </div>
            """

            for _, row in grup.iterrows():
                renk = get_color(row["Verimlilik"])
                tarih = row["Tarih"].strftime("%d.%m.%Y") if pd.notna(row["Tarih"]) else ""

                html += f"""
                <div style='display:flex;padding:6px;border-bottom:1px solid #ddd'>
                    <div style='width:25%'>{row['Operatör']}</div>
                    <div style='width:15%'>{tarih}</div>
                    <div style='width:20%'>{int(row['Çalışılan Dakika'])}</div>
                    <div style='width:20%'>{row['Üretilen Dakika']:.1f}</div>
                    <div style='width:20%;background:{renk};text-align:center'>
                        %{row['Verimlilik']:.2f}
                    </div>
                </div>
                """

        html += "</div>"
        components.html(html, height=800, scrolling=True)

        # 📈 GÜNLÜK GRAFİK
        st.subheader("📈 Günlük Ortalama Verim")
        gunluk = tum_df.groupby("Tarih")["Verimlilik"].mean()
        st.line_chart(gunluk)

        # 📅 HAFTALIK
        st.subheader("📈 Haftalık Ortalama Verim")
        haftalik = tum_df.set_index("Tarih").resample("W")["Verimlilik"].mean()
        st.line_chart(haftalik)

        # 📉 DÜŞÜŞ ALARMI
        st.subheader("📉 Performans Düşüşleri")

        tum_df_sorted = tum_df.sort_values("Tarih")

        dusus_list = []

        for op in tum_df["Operatör"].unique():
            op_df = tum_df_sorted[tum_df_sorted["Operatör"] == op]

            if len(op_df) >= 2:
                son = op_df.iloc[-1]["Verimlilik"]
                onceki = op_df.iloc[-2]["Verimlilik"]

                if son < onceki:
                    dusus_list.append((op, onceki, son))

        if dusus_list:
            for d in dusus_list:
                st.warning(f"{d[0]} düşüşte: %{d[1]:.2f} → %{d[2]:.2f}")
        else:
            st.success("Düşüş yok")

        # 👥 OPERATÖR ANALİZİ
        st.subheader("👥 Operatör Analizi")

        sec_op = st.selectbox("Operatör seç", sorted(tum_df["Operatör"].unique()))

        op_df = tum_df[tum_df["Operatör"] == sec_op]

        if not op_df.empty:
            op_df = op_df.sort_values("Tarih")
            st.line_chart(op_df.set_index("Tarih")["Verimlilik"])

    except Exception as e:
        st.error(f"Hata: {e}")
