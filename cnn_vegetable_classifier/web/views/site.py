from flask import Blueprint, render_template, redirect, url_for, send_file, Response
from flask_login import current_user

from cnn_vegetable_classifier.web import forms
from cnn_vegetable_classifier import models


import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing import image
from io import BytesIO
from PIL import Image
import base64
import io
import imghdr

module = Blueprint("site", __name__)

# test_dir = "/data/test"
# class_names = sorted(os.listdir(test_dir))  # โหลดชื่อคลาสจากโฟลเดอร์ test
# print("Class Names:", class_names)

# โหลดโมเดลเพียงครั้งเดียวเพื่อประสิทธิภาพ
# model_path = "/home/suthinxn/suthinxn/learn/CNN-Vegetable-Classifier/cnn_vegetable_classifier/web/views/my_model.h5"


base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "..", "views", "CNNs_model.h5")  # สร้าง path

print(f"Model path: {os.path.abspath(model_path)}")

# ตรวจสอบว่าไฟล์มีอยู่จริงหรือไม่
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at: {model_path}")

model = tf.keras.models.load_model(model_path)



img_height = 150
img_width = 150


@module.route("/", methods=["GET", "POST"])
def index():

    form =  forms.classifiers.ClassifierForm()
    classifier = models.Classifier()

    if not form.validate_on_submit():
        print("-1-")
        return render_template('/sites/index.html', form=form)

    if form.image.data:
        print("-data-")
        if classifier.image:
            classifier.image.replace(
                form.image.data,
                filename=form.image.data.filename,
                content_type=form.image.data.content_type,
            )
        else:
            classifier.image.put(
                form.image.data,
                filename=form.image.data.filename,
                content_type=form.image.data.content_type,
            )


    form.populate_obj(classifier)
    classifier.save()
    
    classifier = models.Classifier.objects(id=classifier.id).first()

    return redirect(url_for("site.show_result", classifier_id=classifier.id))

# ฟังก์ชันแปลงรูปภาพจาก MongoDB เป็นอาร์เรย์
def get_image_from_db(classifier_id):
    classifier = models.Classifier.objects(id=classifier_id).first()

    img_bytes = classifier.image.read()

    img_data = io.BytesIO(img_bytes)  # ✅ แปลงเป็น Stream
    img = Image.open(img_data).convert("RGB")  # ✅ เปิดภาพ
    img = img.resize((img_width, img_height))  # ✅ ปรับขนาดภาพ
    img_array = image.img_to_array(img) / 255.0  # ✅ Normalize [0,1]
    img_array = np.expand_dims(img_array, axis=0)  # ✅ เปลี่ยนเป็น batch (1, 180, 180, 3)
    return img_array

def predict_image(img_array):
    predictions = model.predict(img_array)
    predicted_index = np.argmax(predictions)
    confidence = float(np.max(predictions))  # ค่าความมั่นใจ
    return predictions, predicted_index, confidence


@module.route("/show_result/<classifier_id>")
def show_result(classifier_id):
    img_array = get_image_from_db(classifier_id)
    classifier = models.Classifier.objects(id=classifier_id).first()

    if img_array is None:
        return "Error: Image not found in database", 404

    predictions, predicted_index, confidence = predict_image(img_array)

    predictions_list = predictions.tolist()[0] 

    class_names = ["Bean", "Bitter_Gourd", "Bottle_Gourd", "Brinjal", "Broccoli", "Cabbage", "Capsicum", "Carrot", "Cauliflower", "Cucumber", "Papaya", "Potato", "Pumpkin", "Radish", "Tomato"]  # ⚠️ แก้เป็น class_names ที่ตรงกับโมเดลของคุณ
    predicted_label = class_names[predicted_index]

    return render_template('/sites/result.html', classifier=classifier, classifier_id=classifier.id, predicted_label=predicted_label, confidence=confidence, labels=class_names, values=predictions_list)

@module.route("/image/<classifier_id>")
def get_image(classifier_id):
    """ ดึงภาพจาก GridFS และส่งกลับเป็น Response """
    classifier = models.Classifier.objects(id=classifier_id).first()
    if classifier and classifier.image:
        image_data = classifier.image.read()
        return Response(image_data, mimetype="image/jpeg")  