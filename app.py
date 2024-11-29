import sqlite3
from tkinter import *
from tkinter import messagebox, ttk

# Koneksi ke database SQLite
conn = sqlite3.connect('library_attendance.db')
cursor = conn.cursor()

# Buat tabel jika belum ada
cursor.execute('''CREATE TABLE IF NOT EXISTS attendance (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    date TEXT NOT NULL,
                    purpose TEXT NOT NULL)''')
conn.commit()

# Fungsi untuk menambahkan data
def add_data():
    name = entry_name.get()
    date = entry_date.get()
    purpose = entry_purpose.get()

    if not name or not date or not purpose:
        messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
        return

    cursor.execute("INSERT INTO attendance (name, date, purpose) VALUES (?, ?, ?)", (name, date, purpose))
    conn.commit()
    messagebox.showinfo("Berhasil", "Data berhasil ditambahkan!")
    clear_entries()
    fetch_data()

# Fungsi untuk mengambil data dari database
def fetch_data():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM attendance")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

# Fungsi untuk menghapus data
def delete_data():
    try:
        selected_item = tree.selection()[0]
        item_id = tree.item(selected_item, 'values')[0]
        cursor.execute("DELETE FROM attendance WHERE id = ?", (item_id,))
        conn.commit()
        messagebox.showinfo("Berhasil", "Data berhasil dihapus!")
        fetch_data()
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang ingin dihapus!")

# Fungsi untuk mengupdate data
def update_data():
    try:
        selected_item = tree.selection()[0]
        item_id = tree.item(selected_item, 'values')[0]

        name = entry_name.get()
        date = entry_date.get()
        purpose = entry_purpose.get()

        if not name or not date or not purpose:
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
            return

        cursor.execute("UPDATE attendance SET name = ?, date = ?, purpose = ? WHERE id = ?", (name, date, purpose, item_id))
        conn.commit()
        messagebox.showinfo("Berhasil", "Data berhasil diubah!")
        clear_entries()
        fetch_data()
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang ingin diubah!")

# Fungsi untuk mencari data
def search_data():
    search_value = entry_search.get()
    if not search_value:
        messagebox.showwarning("Peringatan", "Masukkan kata kunci pencarian!")
        return

    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM attendance WHERE name LIKE ?", ('%' + search_value + '%',))
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", "end", values=row)

# Fungsi untuk membersihkan entri
def clear_entries():
    entry_name.delete(0, END)
    entry_date.delete(0, END)
    entry_purpose.delete(0, END)

# GUI utama
root = Tk()
root.title("Daftar Hadir di Perpustakaan")
root.geometry("800x500")
root.configure(bg="#f7f7f7")

# Header
header_label = Label(root, text="Daftar Hadir di Perpustakaan", font=("Arial", 18, "bold"), fg="black", bg="#f7f7f7")
header_label.pack(pady=10)

# Frame Input
frame_input = Frame(root, bg="#f7f7f7")
frame_input.pack(pady=10)

Label(frame_input, text="Nama:", bg="#f7f7f7", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5, sticky=W)
entry_name = Entry(frame_input, font=("Arial", 12), width=30)
entry_name.grid(row=0, column=1, padx=5, pady=5)

Label(frame_input, text="Tanggal:", bg="#f7f7f7", font=("Arial", 12)).grid(row=1, column=0, padx=5, pady=5, sticky=W)
entry_date = Entry(frame_input, font=("Arial", 12), width=30)
entry_date.grid(row=1, column=1, padx=5, pady=5)

Label(frame_input, text="Keperluan:", bg="#f7f7f7", font=("Arial", 12)).grid(row=2, column=0, padx=5, pady=5, sticky=W)
entry_purpose = Entry(frame_input, font=("Arial", 12), width=30)
entry_purpose.grid(row=2, column=1, padx=5, pady=5)

# Frame Tombol
frame_buttons = Frame(root, bg="#f7f7f7")
frame_buttons.pack(pady=10)

Button(frame_buttons, text="Tambah Data", command=add_data, bg="#4caf50", fg="white", font=("Arial", 12), width=15).grid(row=0, column=0, padx=5)
Button(frame_buttons, text="Ubah Data", command=update_data, bg="#2196f3", fg="white", font=("Arial", 12), width=15).grid(row=0, column=1, padx=5)
Button(frame_buttons, text="Hapus Data", command=delete_data, bg="#f44336", fg="white", font=("Arial", 12), width=15).grid(row=0, column=2, padx=5)

# Frame Pencarian
frame_search = Frame(root, bg="#f7f7f7")
frame_search.pack(pady=10)

Label(frame_search, text="Cari Nama:", bg="#f7f7f7", font=("Arial", 12)).grid(row=0, column=0, padx=5, pady=5)
entry_search = Entry(frame_search, font=("Arial", 12), width=30)
entry_search.grid(row=0, column=1, padx=5, pady=5)

Button(frame_search, text="Cari", command=search_data, bg="#ff9800", fg="white", font=("Arial", 12), width=15).grid(row=0, column=2, padx=5)

# Tabel Data
tree_frame = Frame(root, bg="#f7f7f7")
tree_frame.pack(pady=10)

tree = ttk.Treeview(tree_frame, columns=("ID", "Nama", "Tanggal", "Keperluan"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nama", text="Nama")
tree.heading("Tanggal", text="Tanggal")
tree.heading("Keperluan", text="Keperluan")

tree.column("ID", width=50, anchor=CENTER)
tree.column("Nama", width=200)
tree.column("Tanggal", width=100, anchor=CENTER)
tree.column("Keperluan", width=150)

tree.pack()

fetch_data()

# Entry untuk filter tanggal
label_filter_date = Label(root, text="Filter Tanggal (YYYY-MM-DD):")
label_filter_date.grid(row=4, column=0, padx=10, pady=5)  # Baris ke-4
entry_filter_date = Entry(root)
entry_filter_date.grid(row=4, column=1, padx=10, pady=5)  # Baris ke-4

# Tombol untuk filter tanggal
btn_filter_date = Button(root, text="Filter Tanggal", command=filter_by_date)
btn_filter_date.grid(row=4, column=2, padx=10, pady=5)  # Baris ke-4

# Tombol reset filter
btn_reset_filter = Button(root, text="Reset Filter", command=fetch_data)
btn_reset_filter.grid(row=4, column=3, padx=10, pady=5)  # Baris ke-4

def filter_by_date():
    filter_date = entry_filter_date.get()  # Ambil input dari entry
    cursor.execute("SELECT * FROM attendance WHERE date = ?", (filter_date,))
    rows = cursor.fetchall()
    # Tampilkan hasil filter di tabel atau area yang diinginkan
    display_filtered_data(rows)


# Jalankan aplikasi
root.mainloop()