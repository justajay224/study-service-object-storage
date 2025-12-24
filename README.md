# Service Object Storage

Dokumentasi untuk inisialisasi dan menjalankan projek ini.

## 1. Clone Repository

Jalankan perintah berikut untuk meng-clone repository ini ke komputer lokal:

```bash
git clone https://github.com/justajay224/study-service-object-storage.git
cd study-service-object-storage
```

## 2. Inisialisasi Environment

Disarankan menggunakan virtual environment agar dependencies tidak tercampur dengan sistem global.

### Buat Virtual Environment (jika belum ada)

```bash
# Windows
python -m venv venv

# Mac/Linux
python3 -m venv venv
```

### Aktifkan Virtual Environment

```bash
# Windows (Command Prompt)
venv\Scripts\activate

# Windows (Git Bash/PowerShell)
source venv/Scripts/activate

# Mac/Linux
source venv/bin/activate
```

### Install Dependencies

Setelah virtual environment aktif, install library yang dibutuhkan:

```bash
pip install -r requirements.txt
```

## 3. Menjalankan Aplikasi

Jalankan server menggunakan `uvicorn`:

```bash
uvicorn main:app --reload
```

## 4. Akses API

Setelah server berjalan, dokumentasi API (Swagger UI) dapat diakses di:

http://127.0.0.1:8000/docs
