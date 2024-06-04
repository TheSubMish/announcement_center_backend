from django.conf import settings
from bson.objectid import ObjectId
from .mongodb import database
import uuid
import datetime

def notification(sender,instance,created,**kwargs):
    db = database.connect_db(settings.MONGODB)

    db.notification.insert_one({
        "_id": ObjectId(uuid.uuid4()),
        "sender": sender,
        "receiver": "reciever",
        "message": "message",
        "read": False,
        "created_at": datetime.datetime.now(),
    })