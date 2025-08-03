# 📊 PROJECT 1 : Data Management – HCML

**Description:**  
Documentation and curation of historical data for the **HUSKY-CNOOC Madura Limited (HCML)** project. This includes organizational archives, internal data structures, and a process map of data management workflows in resource exploration and exploitation.

---

## 🧾 Contents

- Data Management Notebook  
- Data Management Analysis  
- Data Management Visualization  
- Data Management Outputs    

---

## 🖼️ Visual Preview

### 📌 Project Preview
<img src="preview/Dokumentasi3.jpg" width="600" alt="Project Preview" style="margin-bottom: 20px;"/>

### 📑 Documentation Preview 1
<img src="preview/Dokumentasi1.jpg" width="600" alt="Documentation Preview 1" style="margin-bottom: 20px;"/>

### 📑 Documentation Preview 2
<img src="preview/Dokumentasi2.jpg" width="600" alt="Documentation Preview 2" style="margin-bottom: 20px;"/>

---

# 📁 PROJECT 2 : File Organizer & Migrator for Downloads Folder

**Description:** 
Proyek ini bertujuan untuk mengelompokkan dan memindahkan file dari folder `Downloads` ke struktur folder baru yang lebih terorganisir berdasarkan jenis file (FileType). Proses ini berguna dalam **manajemen file pribadi**, **migrasi data**, dan **arsip digital**.

---

## 📌 Fitur Utama

- 🔍 Mengelompokkan file berdasarkan `FileType`
- 📂 Membuat struktur folder baru berdasarkan kategori
- 🚚 Memindahkan file hanya jika **file masih ada**
- 🧠 Folder baru hanya dibuat jika memang dibutuhkan (berisi file)
- 📝 Menyimpan **log** file yang tidak ditemukan atau gagal dipindahkan
- ⛏️ Membersihkan folder kosong di `Downloads` setelah proses selesai

---

## 🧾 Struktur Klasifikasi File

| Kategori             | FileType yang Dicakup                                            |
|----------------------|------------------------------------------------------------------|
| Dokumen & Teks       | `document`, `text`, `spreadsheet`, `presentation`, `notebook`, `subtitle` |
| Web & Kode           | `web`, `code`, `config`, `package`, `project`                   |
| Media                | `image`, `video`, `audio`, `design`, `cad`                      |
| GIS & Geoscience     | `gis`, `geoscience`                                              |
| Data & Sistem        | `data`, `system`, `archive`, `security`                         |
| Lainnya              | `unknown`, `lainnya`                                             |

---

## ⚙️ Cara Kerja (Pipeline)

1. **Membaca Dataset**  
   Menggunakan `data_downloads_cleaned.csv` sebagai sumber metadata file.

2. **Mapping Kategori Folder**  
   `MainFolder` dan `Subfolder` ditentukan dari `FileType`.

3. **Filter File yang Masih Ada (Opsional)**  
   Hanya file yang masih tersedia di disk yang akan diproses jika `only_existing_files = True`.

4. **Membuat Folder Tujuan**  
   Folder hanya dibuat jika ada file yang akan dipindahkan ke dalamnya.

5. **Memindahkan File**  
   Menggunakan `shutil.move()` dengan tampilan progres.

6. **Log File Tidak Ditemukan**  
   File yang tidak ditemukan dicatat dalam log `log_file_tidak_ditemukan.csv`.

7. **Menghapus Folder Kosong**  
   Setelah migrasi, folder kosong di `Downloads` akan dihapus otomatis.

---

## 📦 Output

- File tertata rapi di dalam folder tujuan (misalnya: `Documents/Download-Folder-Management`)
- Log file error tersimpan sebagai: `log_file_tidak_ditemukan.csv`


---

## 🚀 Manfaat

- Memudahkan pencarian dan pengelolaan file
- Menghindari kekacauan di folder `Downloads`
- Mendukung efisiensi backup & migrasi data
- Log kesalahan memungkinkan audit file yang bermasalah

---

## 🧠 Catatan

- Pastikan `data_downloads_cleaned.csv` berisi kolom: `Path`, `FileName`, `FileType`.
- Jangan jalankan script ini pada folder penting tanpa backup.
- Folder tujuan harus disesuaikan: `destination_dir`.

---

## 🖼️ Visual Preview

### 📌 Documentation Preview 1
<img src="preview/Dokumentasi14.jpg" width="600" alt="Project Preview" style="margin-bottom: 20px;"/>

### 📑 Documentation Preview 2
<img src="preview/Dokumentasi15.jpg" width="600" alt="Documentation Preview 1" style="margin-bottom: 20px;"/>

---

## 📬 Contact

Fajri Ilham Mughni  
📫 Fajriilhammughni@gmail.com

---

## 📌 License

MIT License