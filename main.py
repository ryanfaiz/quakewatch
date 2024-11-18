import csv
import os

option_file = "options.txt"
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

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def show_banner():
    print("=" * 85)
    print("|               _____           _   _      ___              _                       |")
    print("|              | ____|__ _ _ __| |_| |__  / _ \ _   _  __ _| | _____                |")
    print("|              |  _| / _` | '__| __| '_ \\| | | | | | |/ _` | |/ / _ \\               |")
    print("|              | |__| (_| | |  | |_| | | | |_| | |_| | (_| |   <  __/               |")
    print("|              |_____\__,_|_|   \\__|_| |_|\\__\\_\\__,_|\\__,_|_|\\_\\___|                |")
    print("|                          Sistem Monitoring Gempa Indonesia                        |")
    print("|                       Monitor the Earth, Protect What Matters                     |")
    print("|                                                                                   |")
    print("=" * 85)

def read_all_record():
    '''Membaca semua record yang terdapat di data-gempa.csv, lalu mengembalikannya dalam format list.'''
    with open(csv_file, mode="r", encoding="utf-8-sig") as file:
        reader = csv.reader(file, delimiter=";")
        record = []
        for row in reader:
            record.append(row)
            
    return record

def read_specific_record(waktu_gempa: str):
    '''Membaca data spesifik sesuai parameter waktu_gempa dari semua data. Mengembalikan dalam format list.'''
    records = read_all_record()
    record = []

    for row in records:
        if row and row[0] == waktu_gempa:
            record = row
    
    return record

def read_record_by_region(region: str):
    '''Membaca data sesuai dengan parameter regional. Mengembalikan data dalam bentuk list'''
    records = read_all_record()
    matched_records = []

    for row in records:
        if row and region.lower() in row[5].lower():
            matched_records.append(row)
    
    return matched_records

def minimize_record():
    '''Mengurangi data yang ditampilkan pada kolom tabel dan menampilkannya secara berurutan berdasarkan waktu gempa.'''
    record = read_all_record()
    
    # Membaca status sortir dari file pengaturan
    with open(option_file, "r") as file:
        options = file.read()
        sort_by_time = "sort_by_time=True" in options
        sort_desc = "sort_by_time_desc=True" in options

    # Sortir berdasarkan kolom waktu gempa (indeks ke-0) jika diaktifkan
    if sort_by_time:
        record = sorted(record[1:], key=lambda x: x[0], reverse=sort_desc)
    else:
        record = record[1:]
        
    minimized_record = []
    for row in record:
        filtered_record = [row[i] for i in minimal_headers_index]
        minimized_record.append(filtered_record)
        
    return minimized_record

def show_all_record():
    '''Menampilkan semua data dalam bentuk tabel yang sudah diformat.'''
    record = minimize_record()
    for row in record:         
        formatted_row = "| " + " | ".join(f"{str(item):<{column_widths[i]}}" for i, item in enumerate(row)) + " |"
        print(formatted_row)

def show_specific_record(waktu_gempa: str):
    '''Menampilkan detail spesifik gempa berdasarkan waktu gempa.'''
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
    '''Menampilkan detail gempa terakhir yang terdapat di data-gempa.csv'''
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
    print(f"  Detail: {latest_record[7]}\n")

def create_record(record):
    '''Menambahkan data baru ke dalam data-gempa.csv'''
    current_records = read_all_record()
    
    current_records.insert(1, record)

    with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(current_records)
    
    return "Data berhasil ditambahkan."

def validate_form(record: list):
    '''Melakukan validasi data yang akan ditambahkan'''
    desc = []

    for item in record:
        if item == "":
            desc.append("Data tidak boleh kosong.")
            break

    if record[6] != "Confirmed" and record[6] != "Not Confirmed":
        desc.append("Status tidak sesuai.")

    return desc

def add_record_form():
    '''Formulir pengisian data gempa baru'''
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

def update_record(waktu_gempa: str, updated_record: list):
    '''Memperbarui data gempa berdasarkan parameter waktu_gempa'''
    current_records = read_all_record()

    for index in range(0, len(current_records) - 1, 1):
        if current_records and current_records[index][0] == waktu_gempa:
            current_records[index] = updated_record
    
    with open(csv_file, mode="w", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerows(current_records)

    return "Data berhasil diperbarui."

def update_record_form(waktu_gempa: str):
    '''Formulir pembaruan data gempa'''
    record = read_specific_record(waktu_gempa)

    if not record:
        return print("Data tidak ditemukan.")

    waktu = record[0]
    print(f"Waktu Gempa (UTC): {record[0]}")
    lintang = input(f"Lintang ({record[1]}): ")
    bujur = input(f"Bujur ({record[2]}): ")
    magnitudo = input(f"Magnittudo ({record[3]}): ")
    kedalaman = input(f"Kedalaman (Km) ({record[4]}): ")
    wilayah = input(f"Wilayah ({record[5]}): ")
    status = input(f"Status (Confirmed/Not Confirmed) ({record[6]}): ")
    detail = input(f"Detail (Link BMKG) ({record[7]}): ")

    updated_record = [waktu, lintang, bujur, magnitudo, kedalaman, wilayah, status, detail]

    for i in range(0, len(updated_record) - 1, 1):
        if updated_record[i] == "":
            updated_record[i] = record[i]

    lintang = round(int(lintang), 2)
    bujur = round(int(bujur), 2)
    magnitudo = int(magnitudo)
    kedalaman = int(kedalaman)

    updated_record = [waktu, lintang, bujur, magnitudo, kedalaman, wilayah, status, detail]

    result = update_record(waktu_gempa, updated_record)

    return print(result)

def delete_record(waktu_gempa: str):
    '''Menghapus data gempa spesifik dari data-gempa.csv'''
    current_records = read_all_record()
    new_records = []
    found = False

    for record in current_records:
        if record and record[0] != waktu_gempa:
            new_records.append(record)
        else:
            found = True
    
    if found:
        with open(csv_file, mode="w", newline="") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerows(new_records)
        return print("Data berhasil dihapus.")
    else:
        return print("Data tidak ditemukan.")

def search_record_by_region(region: str):
    '''Mencari data gempa berdasarkan region dan menampilkan dalam bentuk tabel.'''
    record = read_record_by_region(region)

    if not record:
        return print("Data tidak ditemukan.\n") 

    formatted_header = "| " + " | ".join(f"{header:<{column_widths[i]}}" for i, header in enumerate(minimal_headers)) + " |"
    print("=" * len(formatted_header))
    print(formatted_header)
    print("=" * len(formatted_header))

    for row in record:
        if len(row) >= max(minimal_headers_index) + 1:
            formatted_row = "| " + " | ".join(
                f"{str(row[i]):<{column_widths[j]}}" for j, i in enumerate(minimal_headers_index)
            ) + " |"
            print(formatted_row)
        else:
            print("Baris data tidak lengkap:", row) 

    print("=" * len(formatted_header))

def turn_onandoff_sort_by_time():
    '''Fitur flag pada `options.txt` berdasarkan waktu gempa'''
    with open(option_file, "r") as file:
        content = file.read()
    
    if "sort_by_time=True" in content:
        new_content = content.replace("sort_by_time=True", "sort_by_time=False")
    else:
        new_content = content.replace("sort_by_time=False", "sort_by_time=True")

    with open(option_file, "w") as file:
        file.write(new_content)
    
def check_sort_by_time():
    '''Melakukan pengecekkan status fitur flag pada `options.txt`'''
    with open(option_file, "r") as file:
        for line in file:
            if "sort_by_time=True" in line:
                return True

def switch_sort_by_time_desc(switch: str):
    '''Melakukan sort berdasarkan waktu'''
    if switch == "[":
        with open(option_file, "w") as file:
            file.write("sort_by_time=True, sort_by_time_desc=False")
    else:
        with open(option_file, "w") as file:
            file.write("sort_by_time=True, sort_by_time_desc=True")	

def footer():
    '''Menu navigasi sesuai input user'''
    print("=" * 85)
    print("|                                    Opsi Menu                                      |")
    print("-" * 85)
    print("| Tekan: N untuk melihat gempa terbaru        | L untuk melihat daftar gempa        |")
    print("-" * 85)
    print("| Tekan: U untuk memperbarui data gempa       | C untuk membuat data gempa baru     |")
    print("-" * 85)
    print("| Tekan: O untuk melihat detail data gempa    | D untuk menghapus data gempa        |")
    print("-" * 85)
    print("| Tekan: F untuk mencari gempa dengan wilayah | S untuk menyalakan sortir data gempa|")
    print("-" * 85)
    print("| Tekan: E untuk keluar dari aplikasi                                               |")
    if check_sort_by_time():
        print("-" * 85)
        print("| Tekan: [ untuk mengurutkan data gempa berdasarkan waktu gempa terlama             |")
        print("| Tekan: ] untuk mengurutkan data gempa berdasarkan waktu gempa terbaru             |")
    print("=" * 85)

    choice = input("").lower()  # Input dari pengguna sebagai pilihan

    if choice == "[":
        return "["
    elif choice == "]":
        return "]"
    elif choice == "c":
        return "c"
    elif choice == "d":
        return "d"
    elif choice == "f":
        return "f"
    elif choice == "l":
        return "l"
    elif choice == "n":
        return "n"
    elif choice == "o":
        return "o"
    elif choice == "s":
        return "s"
    elif choice == "u":
        return "u"
    elif choice == "e":
        clear_screen()
        print("Terima kasih. Semoga harimu menyenangkan.")
        exit()

    return None

def main():
    '''Menjalankan perulangan dan sebagai logic navigasi'''
    cycle = True
    show_banner()
    show_all_record()
    while cycle:
        action = footer()
        
        if action == "[":
            clear_screen()
            show_banner()
            switch_sort_by_time_desc("[")
            show_all_record()
        elif action == "]":
            clear_screen()
            show_banner()
            switch_sort_by_time_desc("]")
            show_all_record()
        elif action == "c":
            clear_screen()
            show_banner()
            add_record_form()
        elif action == "d":
            clear_screen()
            show_banner()
            show_all_record()
            print()
            waktu_gempa = input("Masukkan Waktu Gempa (UTC) untuk dihapus: ")
            clear_screen()
            show_banner()
            delete_record(waktu_gempa)
        elif action == "f":
            clear_screen()
            show_banner()
            region = input("Masukkan wilayah: ")
            search_record_by_region(region)
        elif action == "l":
            clear_screen()
            show_banner()
            show_all_record()
        elif action == "n":
            clear_screen()
            show_banner()
            show_latest_earthquake()
        elif action == "o":
            clear_screen()
            show_banner()
            show_all_record()
            print()
            waktu_gempa = input("Masukkan Waktu Gempa (UTC) untuk dibuka: ")
            clear_screen()
            show_banner()
            show_specific_record(waktu_gempa)
        elif action == "s":
            clear_screen()
            show_banner()
            show_all_record()
            turn_onandoff_sort_by_time()
        elif action == "u":
            clear_screen()
            show_banner()
            show_all_record()
            print()
            waktu_gempa = input("Masukkan Waktu Gempa (UTC) untuk diperbarui: ")
            clear_screen()
            show_banner()
            update_record_form(waktu_gempa)

if __name__ == "__main__":
    clear_screen()
    main()
