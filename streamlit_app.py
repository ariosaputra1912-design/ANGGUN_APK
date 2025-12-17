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
    def __init__(self, npm, nama, prodi, kelas):
        self.npm = npm
        self.nama = nama
        self.prodi = prodi
        self.kelas = kelas

    def tampil_info(self):
        return f"{self.npm} | {self.nama} | {self.prodi} | {self.kelas}"

    def to_dict(self):
        return self.__dict__

# ==========================
# VALIDATION
# ==========================
def valid_npm(npm):
    return re.fullmatch(r"\d{12}", npm)

def valid_nama(nama):
    return re.fullmatch(r"[A-Za-z ]+", nama)

# ==========================
# SORTING ALGORITHMS (NAMA)
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
# SEARCHING (NPM)
# ==========================
def linear_search(data, npm):
    for m in data:
        if m.npm == npm:
            return m
    return None

def binary_search(data, npm):
    low, high = 0, len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        if data[mid].npm == npm:
            return data[mid]
        elif data[mid].npm < npm:
            low = mid + 1
        else:
            high = mid - 1
    return None

# ==========================
# FILE I/O
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
            st.error("Login gagal")

    st.stop()

# ==========================
# MAIN APP
# ==========================
st.title("🎓 Manajemen Data Mahasiswa")

# ========= INPUT =========
with st.form("input"):
    npm = st.text_input("NPM")
    nama = st.text_input("Nama")
    prodi = st.text_input("Prodi")
    kelas = st.text_input("Kelas")
    submit = st.form_submit_button("Tambah")

    if submit:
        if not valid_npm(npm):
            st.error("NPM harus 12 digit")
        elif not valid_nama(nama):
            st.error("Nama hanya huruf")
        else:
            st.session_state.data.append(
                Mahasiswa(npm, nama, prodi, kelas)
            )
            save_data(st.session_state.data)
            st.success("Data berhasil ditambahkan")

# ========= SORTING =========
st.subheader("🔃 Sorting Berdasarkan Nama")

algoritma = st.selectbox(
    "Pilih Algoritma",
    ["Insertion Sort", "Selection Sort", "Bubble Sort"]
)

arah = st.selectbox(
    "Arah Pengurutan",
    ["Ascending", "Descending"]
)

if st.button("Urutkan Nama"):
    reverse = arah == "Descending"

    if algoritma == "Insertion Sort":
        insertion_sort(st.session_state.data, key=lambda x: x.nama.lower(), reverse=reverse)
    elif algoritma == "Selection Sort":
        selection_sort(st.session_state.data, key=lambda x: x.nama.lower(), reverse=reverse)
    else:
        bubble_sort(st.session_state.data, key=lambda x: x.nama.lower(), reverse=reverse)

    st.success(f"Berhasil diurutkan menggunakan {algoritma}")

# ========= SEARCH =========
st.subheader("🔍 Searching Berdasarkan NPM")

npm_cari = st.text_input("Masukkan NPM")

c1, c2 = st.columns(2)

with c1:
    if st.button("Linear Search"):
        m = linear_search(st.session_state.data, npm_cari)
        if m:
            st.success(m.tampil_info())
        else:
            st.warning("Data tidak ditemukan")

with c2:
    if st.button("Binary Search"):
        # WAJIB urut berdasarkan NPM
        insertion_sort(st.session_state.data, key=lambda x: x.npm)
        m = binary_search(st.session_state.data, npm_cari)
        if m:
            st.success(m.tampil_info())
        else:
            st.warning("Data tidak ditemukan")

# ========= TABLE =========
st.subheader("📋 Data Mahasiswa")
st.dataframe(
    [m.to_dict() for m in st.session_state.data],
    use_container_width=True
)



