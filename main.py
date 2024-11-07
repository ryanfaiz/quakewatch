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


show_banner()