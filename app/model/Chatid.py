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
            "required": ["username", "chatid", "date"],
            "properties": {
                "chatid": {"type": ["string", "null"]},
                "chatid": {"type": ["string", "null"]},
                "chatid": {"type": ["string", "null"]},
            }
        }
