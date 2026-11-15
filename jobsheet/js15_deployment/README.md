# Day vs Night Classifier — Flask + Docker + Hugging Face Spaces

Pipeline deployment hasil JS15: citra → resize 256×256 → grayscale → HOG → `StandardScaler` → MLP (128-64-1) → **Day / Night**.

## Isi folder

| File | Fungsi |
|---|---|
| `app.py` | Web server Flask (port 7860) |
| `requirements.txt` | Dependencies Python |
| `Dockerfile` | Container image (non-root, Python 3.12 slim) |
| `day_night_model.h5` | Model hasil training (dibuat oleh `JS15_*.ipynb`) |
| `scaler.pkl` | Parameter `StandardScaler` hasil training |

> `day_night_model.h5` dan `scaler.pkl` dihasilkan oleh notebook `JS15_244107020095_RACHMAD_FEBRIANANDA.ipynb` pada sel terakhir (Langkah 12). Jalankan notebook tersebut lebih dulu jika kedua file belum ada.

## Menjalankan lokal (tanpa Docker)

```bash
cd jobsheet/js15_deployment
pip install -r requirements.txt
python app.py
# buka http://localhost:7860
```

## Menjalankan dengan Docker

```bash
cd jobsheet/js15_deployment
docker build -t daynight-classifier .
docker run --rm -p 7860:7860 daynight-classifier
# buka http://localhost:7860
```

## Deploy ke Hugging Face Spaces

1. Login ke <https://huggingface.co/>, klik **New Space**.
2. Isi: Space name `daynight-classifier-namaanda`, License MIT, **SDK: Docker**, Template kosong, Visibility Public.
3. Buat **Access Token** dengan permission **Write** (Settings → Access Tokens).
4. Clone repo Space, salin file, lalu push:

```bash
git clone https://huggingface.co/spaces/USERNAME_ANDA/NAMA_SPACE
cd NAMA_SPACE
# salin app.py, requirements.txt, Dockerfile, day_night_model.h5, scaler.pkl ke folder ini
git add .
git commit -m "Deploy Day vs Night classifier"
git push
# Username : username Hugging Face
# Password : Access Token (BUKAN password akun)
```

5. Buka tab **App**, tunggu status berubah dari **Building** menjadi **Running** (3–5 menit).

### Keamanan token

- Jangan menulis token di `app.py`, notebook, README, atau commit history.
- Gunakan credential helper Git atau masukkan saat diminta (`git push`).
- Hapus/revoke token setelah selesai jika tidak dipakai lagi.

## Catatan pengujian

- Uji fungsional Flask dilakukan tanpa Docker (Docker daemon tidak tersedia di mesin penyusunan), memakai `app.test_client()` dengan citra `test/day` dan `test/night`. Hasil: kedua citra terklasifikasi benar.
- Jika container gagal build, cek versi Python pada `Dockerfile` (harus kompatibel dengan `tensorflow-cpu` yang terpasang).