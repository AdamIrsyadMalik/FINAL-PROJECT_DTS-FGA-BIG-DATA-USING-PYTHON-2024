import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Konfigurasi koneksi database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="inventory_system"
)
cursor = db.cursor()

# Fungsi untuk menambah barang
def tambah_barang():
    nama = entry_nama.get()
    jumlah = entry_jumlah.get()
    harga = entry_harga.get()

    if nama and jumlah and harga:
        sql = "INSERT INTO barang (nama, jumlah, harga) VALUES (%s, %s, %s)"
        val = (nama, jumlah, harga)
        cursor.execute(sql, val)
        db.commit()
        messagebox.showinfo("Sukses", "Barang berhasil ditambahkan")
        bersihkan_entry()
        tampilkan_barang()
    else:
        messagebox.showerror("Error", "Semua field harus diisi")

# Fungsi untuk menampilkan barang
def tampilkan_barang():
    tree.delete(*tree.get_children())
    cursor.execute("SELECT * FROM barang")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)

# Fungsi untuk mengupdate barang
def update_barang():
    selected = tree.focus()
    if selected:
        id = tree.item(selected)['values'][0]
        nama = entry_nama.get()
        jumlah = entry_jumlah.get()
        harga = entry_harga.get()

        if nama and jumlah and harga:
            sql = "UPDATE barang SET nama=%s, jumlah=%s, harga=%s WHERE id=%s"
            val = (nama, jumlah, harga, id)
            cursor.execute(sql, val)
            db.commit()
            messagebox.showinfo("Sukses", "Data barang berhasil diupdate")
            bersihkan_entry()
            tampilkan_barang()
        else:
            messagebox.showerror("Error", "Semua field harus diisi")
    else:
        messagebox.showerror("Error", "Pilih barang yang akan diupdate")

# Fungsi untuk menghapus barang
def hapus_barang():
    selected = tree.focus()
    if selected:
        id = tree.item(selected)['values'][0]
        cursor.execute("DELETE FROM barang WHERE id=%s", (id,))
        db.commit()
        messagebox.showinfo("Sukses", "Barang berhasil dihapus")
        reset_auto_increment()
        tampilkan_barang()
    else:
        messagebox.showerror("Error", "Pilih barang yang akan dihapus")

# Fungsi untuk mereset auto increment
def reset_auto_increment():
    cursor.execute("ALTER TABLE barang AUTO_INCREMENT = 1")
    db.commit()

# Fungsi untuk membersihkan entry
def bersihkan_entry():
    entry_nama.delete(0, tk.END)
    entry_jumlah.delete(0, tk.END)
    entry_harga.delete(0, tk.END)

# Fungsi untuk membersihkan semua data
def bersihkan_semua_data():
    if messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus semua data?"):
        cursor.execute("DELETE FROM barang")
        db.commit()
        reset_auto_increment()
        messagebox.showinfo("Sukses", "Semua data telah dihapus")
        tampilkan_barang()

# Fungsi untuk menampilkan grafik stok barang berdasarkan jumlah
def show_chart_jumlah():
    cursor.execute("SELECT nama, jumlah FROM barang")
    data = cursor.fetchall()
    names = [item[0] for item in data]
    amounts = [item[1] for item in data]

    fig, ax = plt.subplots()
    ax.bar(names, amounts)
    ax.set_xlabel('Nama Barang')
    ax.set_ylabel('Jumlah')
    ax.set_title('Jumlah Stok Barang')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=3, column=0, padx=10, pady=10)

# Fungsi untuk menampilkan 10 barang dengan stok tertinggi
def top_10_stok_tertinggi():
    cursor.execute("SELECT nama, jumlah FROM barang ORDER BY jumlah DESC LIMIT 10")
    data = cursor.fetchall()
    display_top_10(data, "Top 10 Stok Barang Tertinggi")

# Fungsi untuk menampilkan 10 barang dengan stok terendah
def top_10_stok_terendah():
    cursor.execute("SELECT nama, jumlah FROM barang ORDER BY jumlah ASC LIMIT 10")
    data = cursor.fetchall()
    display_top_10(data, "Top 10 Stok Barang Terendah")

# Fungsi untuk menampilkan 10 barang dengan harga tertinggi
def top_10_harga_tertinggi():
    cursor.execute("SELECT nama, harga FROM barang ORDER BY harga DESC LIMIT 10")
    data = cursor.fetchall()
    display_top_10(data, "Top 10 Harga Barang Tertinggi")

# Fungsi untuk menampilkan 10 barang dengan harga terendah
def top_10_harga_terendah():
    cursor.execute("SELECT nama, harga FROM barang ORDER BY harga ASC LIMIT 10")
    data = cursor.fetchall()
    display_top_10(data, "Top 10 Harga Barang Terendah")

# Fungsi untuk menampilkan data dalam jendela baru
def display_top_10(data, title):
    top_10_window = tk.Toplevel(root)
    top_10_window.title(title)

    tree_top_10 = ttk.Treeview(top_10_window, columns=("Nama", "Nilai"), show="headings")
    tree_top_10.heading("Nama", text="Nama Barang")
    tree_top_10.heading("Nilai", text="Jumlah/Harga")
    tree_top_10.grid(row=0, column=0, padx=10, pady=10)

    for row in data:
        tree_top_10.insert("", "end", values=row)

# Fungsi untuk menampilkan grafik stok barang berdasarkan harga
def show_chart_harga():
    cursor.execute("SELECT nama, harga FROM barang")
    data = cursor.fetchall()
    names = [item[0] for item in data]
    prices = [item[1] for item in data]

    fig, ax = plt.subplots()
    ax.bar(names, prices)
    ax.set_xlabel('Nama Barang')
    ax.set_ylabel('Harga')
    ax.set_title('Harga Barang')

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().grid(row=3, column=0, padx=10, pady=10)

# Membuat Tampilan Interface
root = tk.Tk()
root.title("Sistem Inventory Management Stok Barang")

# Frame input
frame_input = ttk.Frame(root, padding="10")
frame_input.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame_input, text="Nama Barang:").grid(row=0, column=0, sticky=tk.W)
entry_nama = ttk.Entry(frame_input)
entry_nama.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(frame_input, text="Jumlah:").grid(row=1, column=0, sticky=tk.W)
entry_jumlah = ttk.Entry(frame_input)
entry_jumlah.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(frame_input, text="Harga:").grid(row=2, column=0, sticky=tk.W)
entry_harga = ttk.Entry(frame_input)
entry_harga.grid(row=2, column=1, padx=5, pady=5)

# Tombol-tombol
ttk.Button(frame_input, text="Tambah", command=tambah_barang).grid(row=3, column=0, padx=5, pady=5)
ttk.Button(frame_input, text="Update", command=update_barang).grid(row=3, column=1, padx=5, pady=5)
ttk.Button(frame_input, text="Hapus", command=hapus_barang).grid(row=4, column=0, padx=5, pady=5)
ttk.Button(frame_input, text="Bersihkan", command=bersihkan_entry).grid(row=4, column=1, padx=5, pady=5)

# view untuk menampilkan data
tree = ttk.Treeview(root, columns=("ID", "Nama", "Jumlah", "Harga"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Nama", text="Nama Barang")
tree.heading("Jumlah", text="Jumlah")
tree.heading("Harga", text="Harga")
tree.grid(row=1, column=0, padx=10, pady=10)

# Tombol untuk menampilkan grafik
ttk.Button(root, text="Grafik Jumlah", command=show_chart_jumlah).grid(row=2, column=0, padx=5, pady=5)
ttk.Button(root, text="Grafik Harga", command=show_chart_harga).grid(row=2, column=1, padx=5, pady=5)

# Tombol untuk menampilkan top 10
ttk.Button(root, text="Top 10 Stok Tertinggi", command=top_10_stok_tertinggi).grid(row=5, column=0, padx=5, pady=5)
ttk.Button(root, text="Top 10 Stok Terendah", command=top_10_stok_terendah).grid(row=5, column=1, padx=5, pady=5)
ttk.Button(root, text="Top 10 Harga Tertinggi", command=top_10_harga_tertinggi).grid(row=6, column=0, padx=5, pady=5)
ttk.Button(root, text="Top 10 Harga Terendah", command=top_10_harga_terendah).grid(row=6, column=1, padx=5, pady=5)

# Menampilkan data saat aplikasi dimulai
tampilkan_barang()

root.mainloop()

# Menutup koneksi database saat aplikasi ditutup
db.close()