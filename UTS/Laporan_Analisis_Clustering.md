# Laporan Analisis Perbandingan Metode Clustering
## Dataset Properti — Machine Learning

**Nama:** Rachmad Febriananda | **NIM:** 244107020095

---

## 1. Tujuan

Membandingkan **3 metode clustering** (K-Means, DBSCAN, Hierarchical) × **3 distance metric** (Euclidean, Manhattan, Cosine) secara **adil (fair comparison)**, yaitu dengan **jumlah cluster yang sama (3)** pada semua metode dan parameter yang dipilih melalui prosedur yang jelas:

| Metode | Parameter | Alat Pemilihan |
|---|---|---|
| K-Means | k = 3 | Elbow Method |
| DBSCAN | min_samples = 4 (konsisten), eps per metric | K-Distance Graph + tuning eps |
| Hierarchical | n_clusters = 3, linkage = average | Dendrogram |

---

## 2. Data & Preprocessing

Dataset `dataset_properti.csv` (1.530 data, Jabodetabek). Preprocessing identik di semua eksperimen: hapus ID & duplikat, bersihkan satuan, isi missing value dengan median, hapus outlier ekstrem → **1.498 data**, lalu StandardScaler. Khusus cosine ditambah L2-normalization.

**Fitur clustering (5):** `luas_m2, jumlah_kamar, jumlah_kamar_mandi, usia_bangunan, harga`

> 📷 **[SCREENSHOT 1: Tampilan dataset — df.head()]**

---

## 3. Pemilihan Parameter per Metode

### 3.1 K-Means — Elbow Method → k = 3

Elbow method (k = 2–10) menunjukkan "siku" pada k=3, dikonfirmasi silhouette scan.

> 📷 **[SCREENSHOT 2: Elbow plot K-Means]**
> 📷 **[SCREENSHOT 3: Silhouette score per k — K-Means]**

### 3.2 DBSCAN — K-Distance Graph + Tuning eps

Rule of thumb `min_samples = 2×fitur = 10` menghasilkan solusi degenerate (hanya 1 cluster raksasa, berapapun eps-nya). Karena itu dipakai **min_samples = 4, konsisten untuk ketiga metric**. Nilai eps di-tuning dengan target **tepat 3 cluster**:

| Metric | eps terpilih | Cluster | Noise |
|---|---|---|---|
| Euclidean | 0.8 | 3 | 62 (4.14%) |
| Manhattan | 1.2 | 3 | 52 (3.47%) |
| Cosine | 0.04 | 3 | 72 (4.81%) |

> 📷 **[SCREENSHOT 4: K-distance graph (salah satu metric)]**
> 📷 **[SCREENSHOT 5: Tabel tuning eps — terlihat baris "3 cluster (target tercapai)"]**

### 3.3 Hierarchical — Dendrogram → n_clusters = 3

Dendrogram (average linkage) dipotong pada ketinggian yang menghasilkan 3 cluster. Linkage `average` dipilih karena valid untuk ketiga metric (`ward` hanya berlaku untuk euclidean).

> 📷 **[SCREENSHOT 6: Dendrogram dengan garis potong merah]**

---

## 4. Hasil Perbandingan (9 Kombinasi)

✅ **Semua kombinasi menghasilkan tepat 3 cluster** — syarat fair comparison terpenuhi.

| Metode | Metric | Cluster | Noise | Waktu (s) | Memory (KB) | Silhouette |
|---|---|---|---|---|---|---|
| K-Means | Euclidean | 3 | 0 | 0.379 | 870.6 | 0.2618 |
| K-Means | Manhattan | 3 | 0 | 0.087 | 214.6 | 0.2895 |
| **K-Means** | **Cosine** | **3** | **0** | **0.081** | **212.3** | **0.4496** ⭐ |
| DBSCAN | Euclidean | 3 | 62 | 0.070 | 518.0 | 0.0571 |
| DBSCAN | Manhattan | 3 | 52 | 0.073 | 511.6 | 0.0345 |
| DBSCAN | Cosine | 3 | 72 | 0.107 | 43.954.3 | −0.3548 |
| Hierarchical | Euclidean | 3 | 0 | 0.122 | 9.881.3 | 0.3211 |
| Hierarchical | Manhattan | 3 | 0 | 0.118 | 9.858.6 | 0.2111 |
| Hierarchical | Cosine | 3 | 0 | 0.112 | 9.858.7 | 0.3964 |

> 📷 **[SCREENSHOT 7: Tabel perbandingan 9 metode dari notebook]**
> 📷 **[SCREENSHOT 8: Bar chart Silhouette Score — 9 kombinasi]**
> 📷 **[SCREENSHOT 9: Bar chart waktu eksekusi & memory]**
> 📷 **[SCREENSHOT 10: Scatter plot cluster terbaik (K-Means Cosine)]**

---

## 5. Analisis Hasil

### 5.1 Kualitas cluster (Silhouette)
**K-Means Cosine terbaik (0.4496)**, disusul Hierarchical Cosine (0.3964). Cosine unggul karena pembeda utama antar properti adalah **proporsi/profil fitur** (rasio luas–harga–kamar), bukan besaran absolut — cosine menangkap kesamaan arah vektor. DBSCAN rendah (bahkan negatif pada cosine) karena clusternya timpang: 1 cluster raksasa + 2 cluster kecil, konsekuensi data yang padat menyatu.

### 5.2 Efisiensi
Semua metode cepat (< 0,5 detik). **K-Means paling hemat memori** (±212 KB); Hierarchical boros (±9,9 MB) karena matriks jarak O(n²); DBSCAN Cosine membengkak hingga ±44 MB (matriks jarak pairwise).

### 5.3 Interpretasi cluster (K-Means)
Cluster K-Means seimbang dan mudah diinterpretasi sebagai **3 segmen pasar**, selaras dengan label `kategori_harga` di dataset:

| Cluster | Luas rata² | Kamar | Harga rata² | Dominan | Segmen |
|---|---|---|---|---|---|
| 0 | 70.6 m² | 2.0 | Rp691 jt | 93% Murah | Ekonomis |
| 1 | 112.3 m² | 4.4 | Rp1,38 M | 58% Mahal | Menengah |
| 2 | 161.1 m² | 2.1 | Rp1,87 M | 93% Mahal | Premium |

DBSCAN dan Hierarchical (euclidean/manhattan) cenderung memisahkan **kelompok utama vs properti niche/ekstrem** — berguna untuk deteksi outlier, kurang cocok untuk segmentasi.

> 📷 **[SCREENSHOT 11: Rata-rata fitur per cluster]**
> 📷 **[SCREENSHOT 12: Bar chart komposisi kategori harga per cluster]**

---

## 6. Kesimpulan

1. **Fair comparison tercapai** — 9 kombinasi semuanya menghasilkan 3 cluster, dengan parameter yang dipilih lewat prosedur objektif (elbow, k-distance + tuning, dendrogram).
2. **Distance metric terbaik: Cosine** — unggul pada 2 dari 3 metode.
3. **Metode terbaik: K-Means Cosine** — silhouette tertinggi (0.4496), cluster seimbang dan mudah diinterpretasi (ekonomis/menengah/premium), paling hemat waktu & memori.
4. DBSCAN tetap bermanfaat untuk **deteksi noise/properti tidak biasa** (52–72 data noise); Hierarchical informatif lewat dendrogramnya namun boros memori.

---

**Lampiran:** 9 notebook eksperimen + `Perbandingan_KMeans_DBScan.ipynb` + `hasil_perbandingan_9_metode.csv`
