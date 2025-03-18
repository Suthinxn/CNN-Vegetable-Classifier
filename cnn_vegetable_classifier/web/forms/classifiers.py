from flask_wtf import FlaskForm
from wtforms import SelectField, fields
from wtforms.validators import Optional
from flask_wtf.file import FileAllowed
from flask_mongoengine.wtf import model_form
from cnn_vegetable_classifier.web import models 

BaseClassifierForm = model_form(
    models.Classifier,
    FlaskForm,
    exclude=[],
    field_args={},
)


class ClassifierForm(FlaskForm):
    image = fields.FileField(
        "vegetable image",
        validators=[
            FileAllowed(
                ["png", "jpg", "jpeg"], "ประเภทของไฟล์ไม่ถูกต้อง ต้องเป็น png, jpg และ jpeg"
            )
        ]
    )