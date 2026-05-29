import pandas as pd
import os

def load_all_excels():
    folder_path = "data"

    if not os.path.exists(folder_path):
        print("❌ data folder missing")
        return []

    all_data = []

    for file in os.listdir(folder_path):
        if file.endswith(".xlsx"):
            file_path = os.path.join(folder_path, file)

            print("Reading:", file_path)

            df = pd.read_excel(file_path)

            print("Columns:", df.columns)

            # 🔥 remove completely empty rows
            df = df.dropna(how="all")

            # 🔥 convert everything to string safely
            df = df.astype(str)

            # 🔥 remove garbage rows
            df = df[~df.apply(lambda row: row.astype(str).str.contains("exported from", case=False).any(), axis=1)]

            # 🔥 take only useful rows (non-empty)
            for row in df.values.tolist():

                values = [str(x).strip() for x in row if str(x).strip() != "" and str(x) != "nan"]

                if len(values) >= 2:
                    question = values[0]
                    answer = values[1]

                    all_data.append([question, answer])

    print("FINAL CLEAN DATA:", all_data)

    return all_data