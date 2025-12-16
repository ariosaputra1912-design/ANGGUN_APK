"""
APLIKASI MANAJEMEN DATA MAHASISWA (GUI TKINTER)
Fitur:
- Login GUI
- CRUD Mahasiswa (Tambah, Edit, Hapus)
- Field: NPM, Nama, Prodi, Kelas
- File I/O JSON
- OOP (Encapsulation, Inheritance, Polymorphism)
- Searching (Linear & Binary Search)
- Sorting Nama (Insertion, Selection, Bubble) Ascending/Descending
- Regex Validation
- Exception Handling
- Dark Mode UI
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import re

# ==========================
# OOP BASE CLASS
# ==========================
class Person:
    def tampil_info(self):
        raise NotImplementedError

class Mahasiswa(Person):
    def __init__(self, npm, nama, prodi, kelas):
        self.__npm = npm
        self.__nama = nama
        self.__prodi = prodi
        self.__kelas = kelas

    # Getter
    def get_npm(self): return self.__npm
    def get_nama(self): return self.__nama
    def get_prodi(self): return self.__prodi
    def get_kelas(self): return self.__kelas

    # Setter
    def set_nama(self, nama): self.__nama = nama
    def set_prodi(self, prodi): self.__prodi = prodi
    def set_kelas(self, kelas): self.__kelas = kelas

    # Polymorphism
    def tampil_info(self):
        return f"{self.__npm} | {self.__nama} | {self.__prodi} | {self.__kelas}"

    def to_dict(self):
        return {
            "npm": self.__npm,
            "nama": self.__nama,
            "prodi": self.__prodi,
            "kelas": self.__kelas
        }

# ==========================
# VALIDATION (REGEX)
# ==========================
def valid_npm(npm):
    return re.fullmatch(r"\d{12}", npm)

def valid_nama(nama):
    return re.fullmatch(r"[A-Za-z ]+", nama)

# ==========================
# SORTING ALGORITHMS
# ==========================
def insertion_sort(data, key_func):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and key_func(data[j]) > key_func(key):
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = key

def selection_sort(data, key_func):
    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if key_func(data[j]) < key_func(data[min_idx]):
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]

def bubble_sort(data, key_func):
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if key_func(data[j]) > key_func(data[j + 1]):
                data[j], data[j + 1] = data[j + 1], data[j]

# ==========================
# SEARCHING ALGORITHMS
# ==========================
def linear_search(data, npm):
    for m in data:
        if m.get_npm() == npm:
            return m
    return None

def binary_search(data, npm):
    low, high = 0, len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        if data[mid].get_npm() == npm:
            return data[mid]
        elif data[mid].get_npm() < npm:
            low = mid + 1
        else:
            high = mid - 1
    return None

# ==========================
# FILE I/O
# ==========================
def load_data():
    try:
        with open("data_mahasiswa.json", "r") as f:
            raw = json.load(f)
            return [Mahasiswa(d['npm'], d['nama'], d['prodi'], d['kelas']) for d in raw]
    except:
        return []

def save_data(data):
    try:
        with open("data_mahasiswa.json", "w") as f:
            json.dump([m.to_dict() for m in data], f, indent=4)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ==========================
# LOGIN WINDOW
# ==========================
class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("350x220")
        self.root.configure(bg="#1e1e1e")

        tk.Label(root, text="LOGIN", fg="white", bg="#1e1e1e",
                 font=("Segoe UI", 16, "bold")).pack(pady=15)

        tk.Label(root, text="Username", bg="#1e1e1e", fg="white").pack()
        self.user_entry = tk.Entry(root)
        self.user_entry.pack(pady=5)

        tk.Label(root, text="Password", bg="#1e1e1e", fg="white").pack()
        self.pass_entry = tk.Entry(root, show="*")
        self.pass_entry.pack(pady=5)

        tk.Button(root, text="Login", width=15, bg="#007acc", fg="white",
                  command=self.login).pack(pady=15)

    def login(self):
        if self.user_entry.get() == "anggun" and self.pass_entry.get() == "123":
            self.root.destroy()
            main = tk.Tk()
            App(main)
            main.mainloop()
        else:
            messagebox.showerror("Login Gagal", "Username atau Password salah")

# ==========================
# MAIN APPLICATION
# ==========================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Manajemen Data Mahasiswa")
        self.root.geometry("800x550")
        self.root.configure(bg="#1e1e1e")

        self.data = load_data()

        # INPUT FRAME
        input_frame = tk.LabelFrame(root, text="Input Data", bg="#1e1e1e", fg="white")
        input_frame.pack(fill="x", padx=10, pady=5)

        labels = ["NPM", "Nama", "Prodi", "Kelas"]
        for i, text in enumerate(labels):
            tk.Label(input_frame, text=text, bg="#1e1e1e", fg="white").grid(row=i, column=0, sticky="w", pady=3)

        self.npm_entry = tk.Entry(input_frame)
        self.nama_entry = tk.Entry(input_frame)
        self.prodi_entry = tk.Entry(input_frame)
        self.kelas_entry = tk.Entry(input_frame)

        self.npm_entry.grid(row=0, column=1)
        self.nama_entry.grid(row=1, column=1)
        self.prodi_entry.grid(row=2, column=1)
        self.kelas_entry.grid(row=3, column=1)

        # BUTTON FRAME
        btn_frame = tk.Frame(root, bg="#1e1e1e")
        btn_frame.pack(pady=8)

        tk.Button(btn_frame, text="Tambah", width=12, command=self.tambah).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Edit", width=12, command=self.edit).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Hapus", width=12, command=self.hapus).grid(row=0, column=2, padx=5)

        # SEARCH & SORT FRAME
        ss = tk.LabelFrame(root, text="Search & Sort", bg="#1e1e1e", fg="white")
        ss.pack(fill="x", padx=10, pady=5)

        tk.Label(ss, text="Cari NPM", bg="#1e1e1e", fg="white").grid(row=0, column=0)
        self.search_entry = tk.Entry(ss)
        self.search_entry.grid(row=0, column=1)

        tk.Button(ss, text="Linear", command=self.search_linear).grid(row=0, column=2, padx=5)
        tk.Button(ss, text="Binary", command=self.search_binary).grid(row=0, column=3, padx=5)

        tk.Label(ss, text="Urut Nama", bg="#1e1e1e", fg="white").grid(row=1, column=0, pady=5)
        self.sort_mode = ttk.Combobox(ss, values=["Ascending", "Descending"], state="readonly", width=12)
        self.sort_mode.current(0)
        self.sort_mode.grid(row=1, column=1)

        tk.Button(ss, text="Insertion", command=self.sort_insertion).grid(row=1, column=2)
        tk.Button(ss, text="Selection", command=self.sort_selection).grid(row=1, column=3)
        tk.Button(ss, text="Bubble", command=self.sort_bubble).grid(row=1, column=4)

        # TABLE
        self.tree = ttk.Treeview(root, columns=("NPM", "Nama", "Prodi", "Kelas"), show="headings")
        for col in ("NPM", "Nama", "Prodi", "Kelas"):
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree.bind("<<TreeviewSelect>>", self.isi_form)
        self.refresh()

    # ==========================
    # CRUD
    # ==========================
    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for m in self.data:
            self.tree.insert('', 'end', values=(m.get_npm(), m.get_nama(), m.get_prodi(), m.get_kelas()))

    def tambah(self):
        try:
            npm = self.npm_entry.get()
            nama = self.nama_entry.get()
            prodi = self.prodi_entry.get()
            kelas = self.kelas_entry.get()

            if not valid_npm(npm): raise ValueError("NPM harus 12 digit")
            if not valid_nama(nama): raise ValueError("Nama hanya huruf")

            self.data.append(Mahasiswa(npm, nama, prodi, kelas))
            save_data(self.data)
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def edit(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih data")
            return
        try:
            item = selected[0]
            npm_lama = self.tree.item(item, 'values')[0]
            nama = self.nama_entry.get()
            prodi = self.prodi_entry.get()
            kelas = self.kelas_entry.get()

            if not valid_nama(nama): raise ValueError("Nama hanya huruf")

            for i, m in enumerate(self.data):
                if m.get_npm() == npm_lama:
                    self.data[i] = Mahasiswa(npm_lama, nama, prodi, kelas)
                    break

            save_data(self.data)
            self.refresh()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def hapus(self):
        selected = self.tree.selection()
        if not selected:
            return
        item = selected[0]
        npm = self.tree.item(item, 'values')[0]
        self.data = [m for m in self.data if m.get_npm() != npm]
        save_data(self.data)
        self.refresh()

    # ==========================
    # SEARCH & SORT
    # ==========================
    def search_linear(self):
        m = linear_search(self.data, self.search_entry.get())
        messagebox.showinfo("Hasil", m.tampil_info() if m else "Tidak ditemukan")

    def search_binary(self):
        insertion_sort(self.data, lambda x: x.get_npm())
        m = binary_search(self.data, self.search_entry.get())
        messagebox.showinfo("Hasil", m.tampil_info() if m else "Tidak ditemukan")
        self.refresh()

    def sort_insertion(self):
        insertion_sort(self.data, lambda x: x.get_nama().lower())
        if self.sort_mode.get() == "Descending": self.data.reverse()
        self.refresh()

    def sort_selection(self):
        selection_sort(self.data, lambda x: x.get_nama().lower())
        if self.sort_mode.get() == "Descending": self.data.reverse()
        self.refresh()

    def sort_bubble(self):
        bubble_sort(self.data, lambda x: x.get_nama().lower())
        if self.sort_mode.get() == "Descending": self.data.reverse()
        self.refresh()

    def isi_form(self, event):
        selected = self.tree.selection()
        if not selected: return
        npm, nama, prodi, kelas = self.tree.item(selected[0], 'values')
        self.npm_entry.delete(0, tk.END)
        self.nama_entry.delete(0, tk.END)
        self.prodi_entry.delete(0, tk.END)
        self.kelas_entry.delete(0, tk.END)
        self.npm_entry.insert(0, npm)
        self.nama_entry.insert(0, nama)
        self.prodi_entry.insert(0, prodi)
        self.kelas_entry.insert(0, kelas)

# ==========================
# RUN
# ==========================
if __name__ == '__main__':
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()

