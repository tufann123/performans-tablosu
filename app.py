def parse_excel(df_raw):
    data = []
    current_bolum = None

    for i in range(len(df_raw)):
        row = df_raw.iloc[i]

        col0 = str(row[0]).strip()

        # Bölüm yakala
        if "▶" in col0:
            current_bolum = col0.replace("▶", "").strip()

        # Operatör satırı (isim içeriyor)
        elif current_bolum and col0 not in ["", "None", "nan"]:
            operator = col0

            # sağdaki sayıları bul
            numbers = []
            for val in row:
                try:
                    numbers.append(float(val))
                except:
                    continue

            if len(numbers) >= 2:
                calisilan = numbers[0]
                uretilen = numbers[1]

                data.append([current_bolum, operator, calisilan, uretilen])

    df = pd.DataFrame(data, columns=["Bölüm", "Operatör", "Çalışılan DK", "Üretilen DK"])
    return df
