from flask import Blueprint, render_template, redirect, url_for, Response
from cnn_vegetable_classifier.web import forms
from cnn_vegetable_classifier import models

import tensorflow as tf
import numpy as np
import os
import io
from tensorflow.keras.preprocessing import image
from PIL import Image

# ตั้งค่า Blueprint
module = Blueprint("site", __name__)

# โหลดโมเดล CNN
base_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(base_dir, "..", "views", "CNNs_model.h5")

if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at: {model_path}")

model = tf.keras.models.load_model(model_path)

# กำหนดขนาดรูปภาพที่ใช้ในโมเดล
IMG_HEIGHT, IMG_WIDTH = 150, 150

@module.route("/", methods=["GET", "POST"])
def index():
    """ ฟอร์มอัปโหลดภาพ และบันทึกข้อมูลลง MongoDB """
    form = forms.classifiers.ClassifierForm()
    classifier = models.Classifier()

    if not form.validate_on_submit():
        return render_template('/sites/index.html', form=form)

    if form.image.data:
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

    return redirect(url_for("site.show_result", classifier_id=classifier.id))

def get_image_from_db(classifier_id):
    """ ดึงรูปภาพจาก MongoDB และแปลงเป็นอาร์เรย์ที่ใช้กับโมเดล CNN """
    classifier = models.Classifier.objects(id=classifier_id).first()

    if not classifier or not classifier.image:
        return None

    img_bytes = classifier.image.read()
    img_data = io.BytesIO(img_bytes)
    img = Image.open(img_data).convert("RGB")
    img = img.resize((IMG_WIDTH, IMG_HEIGHT))
    img_array = image.img_to_array(img) / 255.0  # Normalize to [0,1]
    return np.expand_dims(img_array, axis=0)  # เพิ่มมิติให้เป็น batch

def predict_image(img_array):
    """ ทำนายภาพด้วยโมเดล CNN และคืนค่าผลลัพธ์ """
    predictions = model.predict(img_array)
    predicted_index = np.argmax(predictions)
    confidence = float(np.max(predictions))
    return predictions, predicted_index, confidence

@module.route("/show_result/<classifier_id>")
def show_result(classifier_id):
    """ แสดงผลการทำนายภาพ """
    img_array = get_image_from_db(classifier_id)
    classifier = models.Classifier.objects(id=classifier_id).first()

    if img_array is None or classifier is None:
        return "Error: Image not found in database", 404

    predictions, predicted_index, confidence = predict_image(img_array)

    class_names = [
        "Bean", "Bitter_Gourd", "Bottle_Gourd", "Brinjal", "Broccoli", "Cabbage", 
        "Capsicum", "Carrot", "Cauliflower", "Cucumber", "Papaya", "Potato", 
        "Pumpkin", "Radish", "Tomato"
    ]
    predicted_label = class_names[predicted_index]

    return render_template(
        "/sites/result.html", 
        classifier=classifier,
        classifier_id=classifier.id,
        predicted_label=predicted_label,
        confidence=confidence,
        labels=class_names,
        values=predictions.tolist()[0]
    )

@module.route("/image/<classifier_id>")
def get_image(classifier_id):
    """ ดึงภาพจาก MongoDB และส่งกลับเป็น Response """
    classifier = models.Classifier.objects(id=classifier_id).first()
    if classifier and classifier.image:
        return Response(classifier.image.read(), mimetype="image/jpeg")
    return "Image not found", 404
