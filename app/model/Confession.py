from app.model import Model


class Confession(Model.Model):
    def __init__(self, json=None):
        super().__init__(json)
        if json is None:
            json = {"_id": "test"}
        self.json = json
        
        # We set the collection name
        self.set_collection("confession")

        # We set our custom schema
        self.schema = {
            "type": "object",
            "required": [
                "link", 
                "avatar", 
                "author-name", 
                "author-link", 
                "tweet-text", 
                "media"
            ],
            "properties": {
                "link": {"type": "string"},
                "avatar": ["string", "null"],
                "author-name": {"type": "string"},
                "author-link": {"type": "string"},
                "tweet-text": {"type": "string"},
                "media": ["string", "null"],
            }
        }
