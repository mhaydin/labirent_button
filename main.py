import tkinter as tk
from tkinter import ttk
import socket
from datetime import datetime

SERVER_IP = '172.17.0.1'
SERVER_PORT = 12345

STORE_NAMES = [
    "Koton", "Hakan Optik", "Hilal", "Şok Market", "Tavada Tavuk", "D&R", "İpekyol", "Chocolabs", "Mr. Fenomen",
    "Baştacı", "Caccao", "HD İskender", "Burger King", "Esperro Cafe", "Watsons", "Antepeli Lahmacun",
    "Pasaport Pizza", "Sporjinal", "Bursa İshakbey", "Takı Your", "Kılıfçım", "B&G Store", "David Walker",
    "Defacto", "Sport In Street", "Colin's", "Oranj Play House", "Popeyes", "Tuğba", "Cinefora Sinemaları",
    "New City Story", "Çöps", "Arena Fitness", "Nem's Cafe", "Niswom", "Hummel", "English Home", "ARC Trend",
    "Galaktik Evren", "Yves Rocher", "Armağan Oyuncak", "Lufian", "Nüans Terzi", "E-Bebek", "Gratis", "Usta Dönerci",
    "Berru Park", "Flo", "Penti", "Batik", "LC Waikiki", "Altınyıldız Classics", "Dolphin Kuru Temizleme",
    "Atasun Optik", "Avva", "Süvari", "Flyzone", "İkiler", "Eve Shop", "Mavi", "Kitikate", "D'S Damat", "Mi Store",
    "Dido Burger", "Mad Parfüm", "Karaca", "Pro Masaj", "U&ME", "Komagene", "7 Adımda Aşk", "Arby's", "Öncü Döner",
    "Starbucks", "Helvacı Ali", "Bliss Takı", "LegendSide Oyun Merkezi", "Esperro Cafe Kiosk", "Avon"
]

def send_command(command):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, SERVER_PORT))  # Ana bilgisayarın IP adresini burada kullanın
        client_socket.sendall(command.encode())
        client_socket.close()
    except ConnectionRefusedError:
        print("Connection refused. Ensure the server is running and accessible.")

def save_player_info():
    name = name_entry.get()
    surname = surname_entry.get()
    phone = phone_entry.get()
    amount = amount_entry.get()
    store_name = store_var.get()
    if not name or not surname or not phone or not amount or not store_name:
        print("All fields are required.")
        return
    
    try:
        amount = float(amount)
        hak_sayisi = int(amount // 750)
    except ValueError:
        print("Amount must be a number.")
        return
    
    with open("players.txt", "a") as file:
        file.write(f"{datetime.now()}: {name}, {surname}, {phone}, {amount}, {hak_sayisi} hak, {store_name}\n")
    
    send_command(f"START,{hak_sayisi}")
    print(f"Player {name} {surname} saved with {hak_sayisi} hak and start command sent.")
    clear_entries()

def decrement_hak():
    send_command("DECREMENT_HAK")
    print("Hak 1 azaltıldı ve 'Kaybettiniz' komutu gönderildi.")

def clear_entries():
    name_entry.delete(0, tk.END)
    surname_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    store_var.set('')

def filter_stores(event):
    value = store_var.get().lower()
    if value == '':
        store_dropdown['values'] = STORE_NAMES
    else:
        filtered_stores = [store for store in STORE_NAMES if store.lower().startswith(value)]
        store_dropdown['values'] = filtered_stores
        if filtered_stores:
            store_dropdown.set('')
            store_dropdown.event_generate('<Down>')  # Listeyi açar

# Tkinter arayüzü
def create_interface():
    global name_entry, surname_entry, phone_entry, amount_entry, store_var, store_dropdown

    root = tk.Tk()
    root.title("Player Registration")
    root.geometry("400x600")

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("Red.TButton", foreground="white", background="red", padding=(10, 5), font=("Helvetica", 14))

    label = tk.Label(root, text="Player Registration", font=("Helvetica", 16))
    label.pack(pady=10)

    tk.Label(root, text="Name:", font=("Helvetica", 12)).pack()
    name_entry = tk.Entry(root, font=("Helvetica", 12))
    name_entry.pack(pady=5)

    tk.Label(root, text="Surname:", font=("Helvetica", 12)).pack()
    surname_entry = tk.Entry(root, font=("Helvetica", 12))
    surname_entry.pack(pady=5)

    tk.Label(root, text="Phone:", font=("Helvetica", 12)).pack()
    phone_entry = tk.Entry(root, font=("Helvetica", 12))
    phone_entry.pack(pady=5)

    tk.Label(root, text="Alışveriş Tutarı:", font=("Helvetica", 12)).pack()
    amount_entry = tk.Entry(root, font=("Helvetica", 12))
    amount_entry.pack(pady=5)

    tk.Label(root, text="Mağaza İsmi:", font=("Helvetica", 12)).pack()
    store_var = tk.StringVar()
    store_dropdown = ttk.Combobox(root, textvariable=store_var, values=STORE_NAMES, font=("Helvetica", 12))
    store_dropdown.pack(pady=5)
    store_dropdown.bind('<KeyRelease>', filter_stores)

    save_button = tk.Button(root, text="Kaydet", font=("Helvetica", 14), command=save_player_info)
    save_button.pack(pady=20)

    decrement_button = ttk.Button(root, text="Kaybettiniz", style="Red.TButton", command=decrement_hak)
    decrement_button.pack(pady=(10, 10), ipadx=10, ipady=5)

    root.mainloop()

if __name__ == "__main__":
    create_interface()
