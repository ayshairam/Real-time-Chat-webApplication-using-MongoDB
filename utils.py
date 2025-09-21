from db import messages_col
from datetime import datetime

def save_message(sender_email, receiver_email, message):
    messages_col.insert_one({
        "sender": sender_email,
        "receiver": receiver_email,
        "message": message,
        "timestamp": datetime.utcnow()
    })

def get_messages(sender, receiver):
    return list(messages_col.find({
        "$or": [
            {"sender": sender, "receiver": receiver},
            {"sender": receiver, "receiver": sender}
        ]
    }).sort("timestamp", 1))
