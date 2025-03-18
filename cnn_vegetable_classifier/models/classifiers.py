import mongoengine as me

class Classifier(me.Document):
    meta = {"collection" : "classifiers"}

    image = me.ImageField(collection_name="image")