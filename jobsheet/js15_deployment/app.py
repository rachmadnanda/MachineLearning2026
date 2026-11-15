import os
import pickle

import cv2
import numpy as np
import tensorflow as tf
from flask import Flask, request, render_template_string
from skimage.feature import hog

app = Flask(__name__)

MODEL_PATH = os.path.join(os.path.dirname(__file__), 'day_night_model.h5')
SCALER_PATH = os.path.join(os.path.dirname(__file__), 'scaler.pkl')

model = None
scaler = None
try:
    model = tf.keras.models.load_model(MODEL_PATH)
    with open(SCALER_PATH, 'rb') as f:
        scaler = pickle.load(f)
    print('System Loaded Successfully')
except Exception as e:  # pragma: no cover
    print(f'Error loading system: {e}')


def preprocess_image(image_bytes):
    """Preprocessing harus sama persis dengan saat training."""
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError('File gambar tidak dapat dibaca')

    img = cv2.resize(img, (256, 256))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    hog_feat = hog(gray, orientations=9, pixels_per_cell=(8, 8),
                   cells_per_block=(2, 2), block_norm='L2-Hys',
                   visualize=False, feature_vector=True)

    return scaler.transform(hog_feat.reshape(1, -1))


PAGE = '''
<div style="text-align:center; padding:50px; font-family:sans-serif">
    <h1>Day vs Night Classifier</h1>
    <p>Upload gambar, model akan memprediksi siang atau malam.</p>
    <form action="/predict" method="post" enctype="multipart/form-data">
        <input type="file" name="file" accept="image/*" required><br><br>
        <button type="submit">Prediksi</button>
    </form>
</div>
'''


@app.route('/', methods=['GET'])
def home():
    return render_template_string(PAGE)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        file = request.files['file']
        data = preprocess_image(file.read())
        prediction = float(model.predict(data, verbose=0)[0][0])
        label = 'Day (Siang)' if prediction > 0.5 else 'Night (Malam)'
        return (
            "<div style='text-align:center;font-family:sans-serif'>"
            f"<h2>Hasil: {label}</h2>"
            f"<p>P(day) = {prediction:.4f}</p>"
            "<p><a href='/'>Kembali</a></p></div>"
        )
    except Exception as e:
        return f"<h3>Error: {e}</h3><p><a href='/'>Kembali</a></p>"


if __name__ == '__main__':
    # Port 7860 wajib untuk Hugging Face Spaces
    app.run(host='0.0.0.0', port=7860)