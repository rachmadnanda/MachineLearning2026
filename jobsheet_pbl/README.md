# Jobsheet PBL — RumahPoint

Versi PBL dari jobsheet Machine Learning: seluruh materi (JS1–JS7, JS9, JS11, JS13–JS15)
diterapkan pada dataset properti **RumahPoint**, bukan dataset contoh bawaan jobsheet.

## Dataset

`dataset/properti_multi_kota.csv` — 64.650 baris hasil penggabungan beberapa portal
properti nasional (FLUS, 99.co, rumah123, uas-properti).

| Kolom | Keterangan |
|---|---|
| `sumber` | asal data (portal/kota) |
| `lokasi` | kota/kabupaten, ejaan belum seragam |
| `luas_m2` | luas tanah (m²) |
| `luas_bangunan` | luas bangunan (m²), sebagian kosong |
| `jumlah_kamar` | kamar tidur |
| `jumlah_kamar_mandi` | kamar mandi |
| `usia_bangunan` | usia bangunan; sebagian sumber menyimpan tahun bangunan |
| `harga` | harga penawaran (Rupiah) |

Pembersihan yang dipakai konsisten di semua notebook:

1. hapus duplikat;
2. buang outlier (luas 10–2000 m², harga Rp50 juta–Rp100 miliar, kamar ≤ 20);
3. konversi `usia_bangunan` yang berupa tahun (2026 − nilai);
4. turunkan `kondisi` — **Baru** jika usia ≤ 3 tahun, **Bekas** jika > 3 tahun,
   **Tidak diketahui** jika usia kosong;
5. label 3 kelas dari kuantil harga: Murah < Rp483,8 juta, Sedang ≤ Rp1,235 miliar,
   Mahal di atasnya.

Hasil: **56.170 baris**, tiga kelas berimbang (±18,7 ribu per kelas).

> Catatan: `usia_bangunan` hanya terisi pada ±7,7% baris, sehingga `kondisi` didominasi
> `Tidak diketahui` (±92%). Fitur ini disimpan untuk kelengkapan, tetapi kontribusinya
> kecil.

## Daftar notebook

| Notebook | Materi | Metode |
|---|---|---|
| `JS01` | pengenalan, etika data, inspeksi dataset | — |
| `JS02` | praproses | cleaning, imputasi, encoding, scaling |
| `JS03` | seleksi fitur | korelasi, VIF, mutual information, CV |
| `JS04` | clustering | K-Means, elbow, silhouette |
| `JS05` | clustering kepadatan | HDBSCAN |
| `JS06` | pencarian tetangga | Annoy, FAISS, HNSW |
| `JS07` | regresi | linear, polinomial, SVR, Random Forest |
| `JS09` | klasifikasi | k-NN, GaussianNB, BernoulliNB |
| `JS11` | klasifikasi | SVM linear/RBF/poly, GridSearchCV |
| `JS13` | JST | MLP klasifikasi + regresi, ROC/AUC |
| `JS14` | CNN | 1D-CNN pada fitur tabular |
| `JS15` | pipeline & deployment | ColumnTransformer, joblib, Flask |

JS8, JS10, dan JS12 tidak tersedia di repo jobsheet asal sehingga tidak dibuat.

## Cara menjalankan

```bash
cd MachineLearning2026
source .venv/bin/activate   # environment yang dipakai saat notebook dibuat

cd jobsheet_pbl
jupyter nbconvert --to notebook --execute --inplace \
  --ExecutePreprocessor.timeout=3600 JS01_PBL_*.ipynb
```

Di Colab, pasang dependensi terlebih dahulu:

```bash
pip install pandas numpy scikit-learn matplotlib seaborn \
            tensorflow flask joblib annoy faiss-cpu hnswlib
```

Semua notebook memakai path relatif `dataset/properti_multi_kota.csv`, sehingga harus
dijalankan dari folder `jobsheet_pbl/`.

## Artefak deployment

Menjalankan `JS15` akan membuat:

```
deployment/model_harga.joblib
deployment/model_kelas.joblib
deployment/app.py
deployment/requirements.txt
deployment/Dockerfile
```

File `.joblib` tidak di-commit karena dapat dibuat ulang dari notebook. Untuk deploy:

```bash
cd deployment
docker build -t rumahpoint .
docker run -p 7860:7860 rumahpoint
```

Lalu `POST /predict` dengan JSON:

```json
{"lokasi": "Bekasi", "luas_m2": 120, "luas_bangunan": 90,
 "jumlah_kamar": 3, "jumlah_kamar_mandi": 2, "kondisi": "Bekas"}
```