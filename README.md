# CNN-Vegetable-Classifier

6610110341 สุธินันท์ รองพล

[Dataset](https://www.kaggle.com/datasets/misrakahmed/vegetable-image-dataset)

## Installation Guide

 ### 1. Clone Project
โคลนโปรเจกต์จาก GitHub โดยใช้คำสั่งต่อไปนี้:
 `git clone git@github.com:Suthinxn/CNN-Vegetable-Classifier.git`
 
### 2. Set up environment file 
คัดลอกไฟล์ `.env.sample` และเปลี่ยนชื่อเป็น `.env`:

 ### 3. Navigate to the static folder and install dependencies 
 เข้าไปในโฟลเดอร์ `static` และติดตั้งแพ็กเกจที่จำเป็น:
 `cd cnn_vegetable_classifier/web/static/` 
 
คำสั่ง `npm install` จะติดตั้ง dependencies ที่ระบุในไฟล์ `package.json`
- **Linux**: 
	1. ติดตั้ง npm (ถ้ายังไม่ได้ติดตั้ง): 
`sudo apt install npm`
	2. รันคำสั่ง:
	`npm install`
	
- **macOS**:
	1. หากยังไม่ได้ติดตั้ง Node.js และ npm ให้ใช้ Homebrew:
`brew install node`
	2. รันคำสั่ง:
`npm install`

 ### 4. Run the web application:
รันสคริปต์เพื่อเริ่มต้นเว็บแอปพลิเคชัน:
- **Linux**:
 `./scripts/run-web`
-**maxOS**:
 `../scripts/run-web`  
 
 - หมายเหตุ: ตรวจสอบว่าไฟล์ `run-web` มีสิทธิ์ในการรัน (ถ้าไม่มี ให้ใช้ `chmod +x scripts/run-web`) 
