import csv
import os

csv_file = "data-gempa.csv"
headers = [
    "Waktu Gempa (UTC)",
    "Lintang",
    "Bujur",
    "Magnitudo",
    "Kedalaman (Km)",
    "Wilayah",
    "Status",
    "Detail"
]
minimal_headers = ["Waktu Gempa (UTC)", "Magnitudo", "Wilayah", "Status"]
minimal_headers_index = [0,3,5,6]
column_widths = [18, 10, 30, 14]

def show_banner():
    print("=" * 40)
    print("|            EarthQuake                |")
    print("|  Sistem Monitoring Gempa Indonesia   |")
    print("=" * 40)

def read_all_record():
    with open(csv_file, mode="r", encoding="utf-8-sig") as file:
        reader = csv.reader(file, delimiter=";")
        record = []
        for row in reader:
            record.append(row)
            
    return record

def read_specific_record(waktu_gempa: str):
    records = read_all_record()
    record = []

    for row in records:
        if row and row[0] == waktu_gempa:
            record = row
    
    return record

def minimize_record():
    record = read_all_record()
    minimized_record = []
    for row in record:
        filtered_record = []
        for index in minimal_headers_index:
            filtered_record.append(row[index])
        minimized_record.append(filtered_record)

    return minimized_record

def show_all_record():
    record = minimize_record()
    for row in record:         
        # Format and print the filtered row
        formatted_row = "| " + " | ".join(f"{str(item):<{column_widths[i]}}" for i, item in enumerate(row)) + " |"
        print(formatted_row)

def show_specific_record(waktu_gempa: str):
    record = read_specific_record(waktu_gempa)

    if not record:
        return print("Data gempa bumi terakhir tidak ditemukan.")
    
    print("Detail Gempa Bumi")
    print(f"  Waktu Gempa (UTC): {record[0]}")
    print(f"  Lintang: {record[1]}")
    print(f"  Bujur: {record[2]}")
    print(f"  Magnitudo: {record[3]}")
    print(f"  Kedalaman (Km): {record[4]}")
    print(f"  Wilayah: {record[5]}")
    print(f"  Status: {record[6]}")
    print(f"  Detail: {record[7]}")

def show_latest_earthquake():
    records = read_all_record()
    latest_record = records[1]

    if not latest_record:
        return print("Data gempa bumi terakhir tidak ditemukan.")
    
    print("\nGempa Bumi Terkini:")
    print(f"  Waktu Gempa (UTC): {latest_record[0]}")
    print(f"  Lintang: {latest_record[1]}")
    print(f"  Bujur: {latest_record[2]}")
    print(f"  Magnitudo: {latest_record[3]}")
    print(f"  Kedalaman (Km): {latest_record[4]}")
    print(f"  Wilayah: {latest_record[5]}")
    print(f"  Status: {latest_record[6]}")
    print(f"  Detail: {latest_record[7]}")

def create_record(record):
    current_records = read_all_record()
    
    current_records.insert(1, record)

    with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(current_records)
    
    return "Data berhasil ditambahkan."

def validate_form(record: list):
    desc = []

    for item in record:
        if item == "":
            desc.append("Data tidak boleh kosong.")
            break

    if record[6] != "Confirmed" and record[6] != "Not Confirmed":
        desc.append("Status tidak sesuai.")

    return desc

def add_record_form():
    waktu = input("Waktu Gempa (UTC) (DD/MM/YYYY HH:MM): ")
    lintang = input("Lintang: ")
    bujur = input("Bujur: ")
    magnitudo = input("Magnittudo: ")
    kedalaman = input("Kedalaman (Km): ")
    wilayah = input("Wilayah: ")
    status = input("Status (Confirmed/Not Confirmed): ")
    detail = input("Detail (Link BMKG): ")

    record = [waktu, lintang, bujur, magnitudo, kedalaman, wilayah, status, detail]

    result = validate_form(record)

    if result:
        for desc in result:
            print(desc)
        print("1. Coba lagi")
        print("2. Kembali ke menu utama")
        nav = int(input("Pilih opsi (1-2): "))
        if nav == 1:
            add_record_form()
        else:
            return
    lintang = round(int(lintang), 2)
    bujur = round(int(bujur), 2)
    magnitudo = int(magnitudo)
    kedalaman = int(kedalaman)

    record = [waktu, lintang, bujur, magnitudo, kedalaman, wilayah, status, detail]

    result = create_record(record)
    
    return print(result)


show_banner()
show_latest_earthquake()