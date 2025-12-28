# File Service - Object Storage

Service untuk upload dan akses file dengan enkripsi AES-256. File disimpan di Backblaze B2 cloud storage.

## Fitur

- ✅ Upload file (async/background)
- ✅ Download file langsung (sebagai URL)
- ✅ Enkripsi AES-256 GCM
- ✅ Pre-cache untuk response cepat
- ✅ Validasi file type (images & documents)

---

## Setup untuk Development

### 1. Clone Repository

### 2. Buat Virtual Environment

```bash
python -m venv venv
```

### 3. Aktifkan Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Windows (Git Bash) / Linux / Mac:**
```bash
source venv/Scripts/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Konfigurasi Environment

Copy `.env-sample` ke `.env` dan isi nilainya:

```bash
cp .env-sample .env
```

Isi file `.env`:
```env
BACKBLAZE_KEY_ID=your_key_id
BACKBLAZE_APPLICATION_KEY=your_app_key
BACKBLAZE_BUCKET_NAME=your_bucket_name
ENCRYPTION_KEY=your_32_byte_key_in_base64
BASE_URL=http://127.0.0.1:8000
PORT=8000
```

> **Note:** `ENCRYPTION_KEY` harus 32 bytes dalam format base64 untuk AES-256.

### 6. Jalankan Server

```bash
python main.py
```

## Panduan untuk Frontend (Nuxt/Vue)

### Upload File (Async)

Upload berjalan di background, response langsung (~100ms).

**1. POST `/file/upload`**

Request:
```javascript
const formData = new FormData()
formData.append('file', fileInput.files[0])

const response = await fetch('http://api/file/upload', {
  method: 'POST',
  body: formData
})
const result = await response.json()
// result.data = { tempId, status, checkStatusUrl }
```

Response (202 Accepted):
```json
{
  "metaData": { "message": "Upload started", "code": 202 },
  "data": {
    "tempId": "abc-123-uuid",
    "status": "uploading",
    "checkStatusUrl": "http://api/file/status/abc-123-uuid"
  }
}
```

**2. Poll Status - GET `/file/status/{tempId}`**

```javascript
const poll = setInterval(async () => {
  const res = await fetch(`http://api/file/status/${tempId}`)
  const data = await res.json()
  
  if (data.data.status === 'completed') {
    clearInterval(poll)
    // Gunakan data.data.link untuk akses file
    console.log('File URL:', data.data.link)
  }
}, 1000) // Poll setiap 1 detik
```

Response saat completed:
```json
{
  "metaData": { "message": "Upload completed", "code": 200 },
  "data": {
    "status": "completed",
    "fileId": "4_xxx...",
    "link": "http://api/file/4_xxx..."
  }
}
```

**3. Akses File**

Link yang didapat bisa langsung digunakan:
```html
<img :src="fileLink" alt="uploaded image" />
```

### Update File (Async)

Update juga berjalan di background, pattern sama dengan upload.

**1. PUT `/file/update/{fileId}`**

Request:
```javascript
const formData = new FormData()
formData.append('file', newFileInput.files[0])

const response = await fetch(`http://api/file/update/${oldFileId}`, {
  method: 'PUT',
  body: formData
})
const result = await response.json()
// result.data = { tempId, status, checkStatusUrl }
```

Response (202 Accepted):
```json
{
  "metaData": { "message": "Update started", "code": 202 },
  "data": {
    "tempId": "def-456-uuid",
    "status": "updating",
    "checkStatusUrl": "http://api/file/status/def-456-uuid"
  }
}
```

**2. Poll status sama seperti upload** - Tunggu sampai `status: "completed"`

---

### Endpoints Summary

| Method | Endpoint | Deskripsi |
|--------|----------|-----------|
| POST | `/file/upload` | Upload file (async) |
| PUT | `/file/update/{fileId}` | Update file (async) |
| GET | `/file/status/{tempId}` | Cek status upload/update |
| GET | `/file/{fileId}` | Akses file langsung |
| GET | `/file/all-files` | List semua file |
| DELETE | `/file/delete/{fileId}` | Hapus file |

---

### Allowed File Types

- **Images:** `.png`, `.jpg`, `.jpeg`, `.webp`, `.svg`
- **Documents:** `.pdf`, `.doc`, `.docx`
- **Max size:** 10MB

---

### Response Format

Semua response mengikuti format:
```json
{
  "metaData": {
    "message": "...",
    "code": 200,
    "response_code": "0000"
  },
  "data": { ... }
}
```

---

## Notes

- File di-cache setelah upload, sehingga GET pertama kali juga cepat
- Cache menyimpan max 100 file (LRU eviction)
- File terlalu besar (>10MB) tidak di-cache
