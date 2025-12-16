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
# SEARCH & SORT
# ==========================
def linear_search(data, npm):
    for m in data:
        if m.npm == npm:
            return m
    return None

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
            st.success("Data ditambahkan")

# ==========================
# TABLE
# ==========================
st.subheader("📋 Data Mahasiswa")
st.dataframe(
    [m.to_dict() for m in st.session_state.data],
    use_container_width=True
)

# ==========================
# SEARCH
# ==========================
st.subheader("🔎 Cari Mahasiswa")
npm_cari = st.text_input("Cari NPM")

if st.button("Cari"):
    m = linear_search(st.session_state.data, npm_cari)
    if m:
        st.success(m.tampil_info())
    else:
        st.warning("Tidak ditemukan")


