from app.model import *


class Chatid(Model.Model):
    def __init__(self, json=None):
        super().__init__(json)
        if json is None:
            json = {"_id": "test"}
        self.json = json
        
        # We set the collection name
        self.set_collection("chatid")

        # We set our custom schema
        self.schema = {
            "type": "object",
            "required": ["username", "chat-id", "status", "date"],
            "properties": {
                "username": {"type": ["string", "null"]},
                "chat-id": {"type": ["string", "null"]},
                "status": {"type": ["string", "null"]},
                "date": {"type": ["string", "null"]},
            }
        }
