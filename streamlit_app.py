import streamlit as st
import json
import re

# ==========================
# OOP
# ==========================
class Person:
    def tampil_info(self):
        raise NotImplementedError

class Mahasiswa(Person):
    def __init__(self, nim, nama, prodi, kelas):
        self.nim = nim
        self.nama = nama
        self.prodi = prodi
        self.kelas = kelas

    def tampil_info(self):
        return f"{self.nim} | {self.nama} | {self.prodi} | {self.kelas}"

    def to_dict(self):
        return self.__dict__

# ==========================
# VALIDATION (REGEX)
# ==========================
def valid_nim(nim):
    return re.fullmatch(r"\d{12}", nim)

def valid_nama(nama):
    return re.fullmatch(r"[A-Za-z ]+", nama)

# ==========================
# SORTING (BERDASARKAN NAMA)
# ==========================
def insertion_sort(data, key, reverse=False):
    for i in range(1, len(data)):
        temp = data[i]
        j = i - 1
        while j >= 0 and key(data[j]) > key(temp):
            data[j + 1] = data[j]
            j -= 1
        data[j + 1] = temp
    if reverse:
        data.reverse()

def selection_sort(data, key, reverse=False):
    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if key(data[j]) < key(data[min_idx]):
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
    if reverse:
        data.reverse()

def bubble_sort(data, key, reverse=False):
    n = len(data)
    for i in range(n):
        for j in range(0, n - i - 1):
            if key(data[j]) > key(data[j + 1]):
                data[j], data[j + 1] = data[j + 1], data[j]
    if reverse:
        data.reverse()

# ==========================
# SEARCHING (BERDASARKAN NIM)
# ==========================
def linear_search(data, nim):
    for m in data:
        if m.nim == nim:
            return m
    return None

def binary_search(data, nim):
    low, high = 0, len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        if data[mid].nim == nim:
            return data[mid]
        elif data[mid].nim < nim:
            low = mid + 1
        else:
            high = mid - 1
    return None

# ==========================
# FILE I/O JSON
# ==========================
def load_data():
    try:
        with open("data_mahasiswa.json") as f:
            raw = json.load(f)
            return [Mahasiswa(**d) for d in raw]
    except:
        return []

def save_data(data):
    with open("data_mahasiswa.json", "w") as f:
        json.dump([m.to_dict() for m in data], f, indent=4)

# ==========================
# SESSION STATE
# ==========================
if "login" not in st.session_state:
    st.session_state.login = False

if "data" not in st.session_state:
    st.session_state.data = load_data()

# ==========================
# LOGIN
# ==========================
if not st.session_state.login:
    st.title("🔐 Login")

    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):
        if user == "anggun" and pw == "123":
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Username atau password salah")

    st.stop()

# ==========================
# MAIN APP
# ==========================
st.title("🎓 Manajemen Data Mahasiswa")

# ==========================
# TAMBAH DATA
# ==========================
st.subheader("➕ Tambah Data Mahasiswa")

with st.form("tambah"):
    nim = st.text_input("NIM")
    nama = st.text_input("Nama")
    prodi = st.text_input("Prodi")
    kelas = st.text_input("Kelas")
    simpan = st.form_submit_button("Tambah")

    if simpan:
        if not valid_nim(nim):
            st.error("NIM harus 12 digit")
        elif not valid_nama(nama):
            st.error("Nama hanya huruf")
        else:
            st.session_state.data.append(
                Mahasiswa(nim, nama, prodi, kelas)
            )
            save_data(st.session_state.data)
            st.success("Data berhasil ditambahkan")
            st.rerun()

# ==========================
# EDIT DATA
# ==========================
st.subheader("✏️ Edit Data Mahasiswa")

nim_edit = st.selectbox(
    "Pilih NIM",
    [""] + [m.nim for m in st.session_state.data]
)

if nim_edit:
    mhs = next(m for m in st.session_state.data if m.nim == nim_edit)

    with st.form("edit"):
        nama_baru = st.text_input("Nama", value=mhs.nama)
        prodi_baru = st.text_input("Prodi", value=mhs.prodi)
        kelas_baru = st.text_input("Kelas", value=mhs.kelas)
        update = st.form_submit_button("Simpan Perubahan")

        if update:
            if not valid_nama(nama_baru):
                st.error("Nama hanya huruf")
            else:
                mhs.nama = nama_baru
                mhs.prodi = prodi_baru
                mhs.kelas = kelas_baru
                save_data(st.session_state.data)
                st.success("Data berhasil diperbarui")
                st.rerun()

# ==========================
# HAPUS DATA
# ==========================
st.subheader("🗑 Hapus Data Mahasiswa")

nim_hapus = st.selectbox(
    "Pilih NIM yang akan dihapus",
    [""] + [m.nim for m in st.session_state.data],
    key="hapus"
)

if nim_hapus:
    if st.button("Hapus Data"):
        st.session_state.data = [
            m for m in st.session_state.data if m.nim != nim_hapus
        ]
        save_data(st.session_state.data)
        st.success("Data berhasil dihapus")
        st.rerun()

# ==========================
# SORTING
# ==========================
st.subheader("🔃 Sorting Berdasarkan Nama")

algoritma = st.selectbox(
    "Algoritma",
    ["Insertion Sort", "Selection Sort", "Bubble Sort"]
)

arah = st.selectbox(
    "Arah",
    ["Ascending", "Descending"]
)

if st.button("Urutkan"):
    reverse = arah == "Descending"

    if algoritma == "Insertion Sort":
        insertion_sort(st.session_state.data, key=lambda x: x.nama.lower(), reverse=reverse)
    elif algoritma == "Selection Sort":
        selection_sort(st.session_state.data, key=lambda x: x.nama.lower(), reverse=reverse)
    else:
        bubble_sort(st.session_state.data, key=lambda x: x.nama.lower(), reverse=reverse)

    st.success("Data berhasil diurutkan")

# ==========================
# SEARCHING
# ==========================
st.subheader("🔍 Searching Berdasarkan NIM")

nim_cari = st.text_input("Masukkan NIM")

c1, c2 = st.columns(2)

with c1:
    if st.button("Linear Search"):
        m = linear_search(st.session_state.data, nim_cari)
        st.success(m.tampil_info()) if m else st.warning("Data tidak ditemukan")

with c2:
    if st.button("Binary Search"):
        insertion_sort(st.session_state.data, key=lambda x: x.nim)
        m = binary_search(st.session_state.data, nim_cari)
        st.success(m.tampil_info()) if m else st.warning("Data tidak ditemukan")

# ==========================
# TABLE
# ==========================
st.subheader("📋 Data Mahasiswa")
st.dataframe(
    [m.to_dict() for m in st.session_state.data],
    use_container_width=True
)
