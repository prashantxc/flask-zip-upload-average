import os
import csv

def process_folder(folder_path):
    row_index = 17
    column_index = ord('S') - ord('A')
    values = []

    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith('.csv'):
                file_path = os.path.join(root, filename)
                with open(file_path, 'r', newline='') as f:
                    reader = list(csv.reader(f))
                    try:
                        bekaar_value = reader[row_index][column_index].replace('%', '').strip()
                        value = float(bekaar_value)
                        values.append(value)
                    except (IndexError, ValueError):
                        print(f"Skipping {filename}")
                        continue

    if values:
        average = sum(values) / len(values)
        return f"Processed {len(values)} files. Average of column S (row 18): {average:.2f}%"
    else:
        return "No valid CSV file found or data missing."
