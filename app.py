from flask import Flask, request, jsonify,render_template
import base64
from io import BytesIO
from PIL import Image
import os
from tensorflow.keras.models import load_model
from keras.preprocessing.image import load_img, img_to_array
import tensorflow as tf
import numpy as np

#Modeli Yüklemek ve Flask Uygulmasının temelini oluşturmak için
app = Flask(__name__)
model = load_model('Drawing_Model.h5')

# Resimlerin kaydedileceği dizin
UPLOAD_FOLDER = './images_folder'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/kaydet', methods=['POST'])
def kaydet():
    try:
        # JSON verisini almak için
        data = request.get_json()
        image_data = data['image']

        # Base64 kodunu çöz
        image_data = image_data.split(',')[1]  # "data:image/png;base64," kısmını kaldır
        image_bytes = base64.b64decode(image_data)

        # Resmi kaydet ve tahmin işlemini yap
        image = Image.open(BytesIO(image_bytes))
        image.save(os.path.join(UPLOAD_FOLDER, 'Drawing_image.png'))
        image_path= "./images_folder/Drawing_image.png"
        image = load_img(image_path, target_size=(256, 256))
        image_array = img_to_array(image)
        exp_dim = tf.expand_dims(image_array,0)
        predictions = model.predict(exp_dim)
        result = tf.nn.softmax(predictions[0])

        #Türkçe karakterli yeni dizi
        drawing_names = ['Elma', 'Muz', 'Basketbol', 'Brokoli', 'Süpürge', 'Otobüs', 'Kamera',
                    'Havuç', 'Sandalye', 'Daire', 'Bulut', 'Kapı', 'Çiçek', 'El', 'Merdiven',
                    'Armut', 'Ananas', 'Gökkuşağı', 'Kare', 'Yıldız', 'Güneş', 'Üçgen']

        outcome = str(np.max(result)*100) + "% oranla "+ drawing_names[np.argmax(result)] + " olduğunu düşünüyorum..."
        return jsonify({'message': outcome})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)