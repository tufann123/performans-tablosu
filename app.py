for sheet in sheet_names:

    df = pd.read_excel(uploaded_file, sheet_name=sheet)

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

    # 🔵 BÖLÜM BAŞLIK
    html += f"""
    <div style='background:#2f6690;color:white;padding:10px;margin-top:15px;font-weight:bold'>
    ▶ {sheet.upper()} - %{ort_verim:.1f}
    </div>
    """

    # ✅ TABLO BAŞLIĞI EKLENDİ
    html += """
    <div style='display:flex;font-weight:bold;background:#eaeaea;
