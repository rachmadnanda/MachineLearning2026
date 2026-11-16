import os
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, request

BASE = Path(__file__).resolve().parent

model_harga = joblib.load(BASE / 'model_harga.joblib')
model_kelas = joblib.load(BASE / 'model_kelas.joblib')

app = Flask(__name__)

KOLOM = ['luas_m2', 'luas_bangunan', 'jumlah_kamar',
         'jumlah_kamar_mandi', 'lokasi', 'kondisi']
DEFAULT = {
    'luas_m2': 100.0,
    'luas_bangunan': 65.0,
    'jumlah_kamar': 2.0,
    'jumlah_kamar_mandi': 2.0,
    'lokasi': 'Tidak diketahui',
    'kondisi': 'Tidak diketahui',
}


@app.get('/')
def index():
    return jsonify({
        'status': 'ok',
        'model': 'RumahPoint Random Forest',
        'field': KOLOM,
        'contoh': {
            'lokasi': 'Bekasi',
            'luas_m2': 120,
            'luas_bangunan': 90,
            'jumlah_kamar': 3,
            'jumlah_kamar_mandi': 2,
            'kondisi': 'Bekas',
        },
    })


@app.post('/predict')
def predict():
    data = request.get_json(force=True, silent=True) or {}
    baris = {k: data.get(k, v) for k, v in DEFAULT.items()}
    frame = pd.DataFrame([baris])

    log_harga = float(model_harga.predict(frame)[0])
    harga = float(10 ** log_harga)
    kategori = str(model_kelas.predict(frame)[0])

    return jsonify({
        'harga_prediksi': round(harga),
        'harga_juta': round(harga / 1e6, 1),
        'kategori': kategori,
        'input': baris,
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 7860)))
