from django.contrib.sessions.backends.base import SessionBase
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from pymongo import MongoClient

class MongoDBSessionStore(SessionBase):

    
    def __init__(self, session_key=None):
        super().__init__(session_key)
        self.client = MongoClient(settings.MONGO_URI)
        self.db = self.client[settings.SESSION_DATABASE]
        self.collection = self.db[settings.SESSION_COLLECTION]

    def load(self):
        """Load session data from MongoDB."""
        session_data = self.collection.find_one({"session_key": self.session_key})
        if session_data:
            return self.decode(session_data["session_data"])
        return {}

    def exists(self, session_key):
        """Check if session exists in MongoDB."""
        return self.collection.find_one({"session_key": session_key}) is not None

    def create(self):
        """Create a new session in MongoDB."""
        self.session_key = self._get_new_session_key()
        self.collection.insert_one({
            "session_key": self.session_key,
            "session_data": self.encode({}),
            "expire_date": self.get_expiry_date()
        })
        self.modified = True

    def save(self, must_create=False):
        """Save session data to MongoDB."""
        if must_create:
            self.create()
        self.collection.update_one(
            {"session_key": self.session_key},
            {"$set": {
                "session_data": self.encode(self._get_session(no_load=must_create)),
                "expire_date": self.get_expiry_date()
            }},
            upsert=True
        )

    def delete(self, session_key=None):
        """Delete a session from MongoDB."""
        if session_key is None:
            session_key = self.session_key
        self.collection.delete_one({"session_key": session_key})
