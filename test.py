import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing import image

# โหลดโมเดลที่ฝึกไว้
model = tf.keras.models.load_model("my_model.h5")

# พาธของโฟลเดอร์ test
test_dir = "data/test"

# ดึงชื่อคลาสจาก test dataset
class_names = sorted(os.listdir(test_dir))  # ใช้ sorted() เพื่อเรียงลำดับโฟลเดอร์
print("Class Names:", class_names)

# กำหนดขนาดภาพ
img_height = 150
img_width = 150

def predict_image(img_path):
    """ โหลดภาพจากพาธ, ทำการพยากรณ์ และแสดงผล """
    img = image.load_img(img_path, target_size=(img_height, img_width))
    img_array = image.img_to_array(img) / 255.0  # Normalize
    img_array = np.expand_dims(img_array, axis=0)  # แปลงเป็น batch (1, 150, 150, 3)

    # พยากรณ์
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions)  # ดึง index ของ class ที่มีค่ามากที่สุด
    confidence = np.max(predictions)  # ความมั่นใจ

    return class_names[predicted_class], confidence

# ✅ พยากรณ์ทุกภาพในแต่ละโฟลเดอร์ของ test
for folder in class_names:
    folder_path = os.path.join(test_dir, folder)
    if not os.path.isdir(folder_path):
        continue  # ข้ามหากไม่ใช่โฟลเดอร์

    print(f"\n🔍 Predicting images in folder: {folder}")
    
    for img_name in os.listdir(folder_path):
        img_path = os.path.join(folder_path, img_name)
        predicted_label, confidence = predict_image(img_path)
        
        print(f"📌 Image: {img_name} | Predicted: {predicted_label} | Confidence: {confidence:.2f}")
