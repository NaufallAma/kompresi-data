# 📦 Project Kompresi Data

## 👨‍💻 Anggota Tim
 ___________________________________________________
| Nama Lengkap                |           NIM       |
|-----------------------------|---------------------|
| Naufal Danendra Amanullah   |      231240001425   |
| Naffahal Lucky Mubarok      |      231240001423   |
|_____________________________|_____________________|

## 🚀 Deskripsi Singkat
Aplikasi ini adalah aplikasi **kompresi data berbasis web** yang dapat mengompresi berbagai jenis file seperti gambar (.jpg, .png), dokumen (.pdf, .docx, .pptx) dengan mudah melalui browser.  
Proyek ini dikembangkan untuk membantu memperkecil ukuran file agar lebih efisien dalam penyimpanan maupun pengiriman data.

## 🛠 Teknologi yang Digunakan
- **Backend**: Python Flask
- **Frontend**: HTML & Tailwind CSS
- **Library Kompresi**:
  - Pillow → kompresi gambar (.jpg, .png)
  - PyMuPDF (fitz) → kompresi PDF
  - zipfile + recompress → kompresi gambar dalam .docx / .pptx
- **Environment**: Python Virtual Environment (venv)
- **Editor**: VS Code / PyCharm

## 🔄 Alur Aplikasi
1. Pengguna membuka halaman web aplikasi.
2. Mengunggah file yang ingin dikompresi.
3. Memilih tingkat kualitas kompresi (Tinggi, Sedang, Rendah).
4. Server Flask memproses kompresi berdasarkan jenis file.
5. Menampilkan ukuran file sebelum dan sesudah.
6. Pengguna dapat mengunduh hasil file yang sudah dikompresi.
