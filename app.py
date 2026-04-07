def parse_excel(df_raw):
    data = []
    current_bolum = None

    for i in range(len(df_raw)):
        row = df_raw.iloc[i]

        # tüm hücreleri string yap
        row_values = [str(x).strip() for x in row if str(x) != "nan"]

        if not row_values:
            continue

        text = " ".join(row_values).upper()

        # BÖLÜM YAKALA (anahtar kelimeler)
        if any(b in text for b in ["SEİRİM", "KESİM", "HAVLU", "PAKET", "KALİTE"]):
            for b in ["SEİRİM", "KESİM", "HAVLU", "PAKET", "KALİTE"]:
                if b in text:
                    current_bolum = b
                    break

        # OPERATÖR + SAYI YAKALA
        elif current_bolum:
            numbers = []
            operator = None

            for val in row:
                try:
                    numbers.append(float(val))
                except:
                    if isinstance(val, str) and val.strip() != "":
                        operator = val.strip()

            if operator and len(numbers) >= 2:
                data.append([current_bolum, operator, numbers[0], numbers[1]])

    df = pd.DataFrame(data, columns=["Bölüm", "Operatör", "Çalışılan DK", "Üretilen DK"])
    return df
