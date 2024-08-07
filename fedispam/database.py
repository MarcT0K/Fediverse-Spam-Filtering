import dbm

from asyncio import Lock


class Database:
    def __init__(self, db_filename):
        self._lock = Lock()
        self.db_filename = db_filename
        self._db = None

    def open(self):
        self._db = dbm.open(self.db_filename, "c")

    def close(self):
        if self._db is not None:
            self._db.close()

    def extract_db(self):
        assert self._db is not None
        db_dict = {key: self._db[key] for key in self._db.keys()}
        return db_dict

    async def get_key(self, key):
        assert self._db is not None
        async with self._lock:
            val = self._db[key]
        return val

    async def get_and_del_key(self, key):
        assert self._db is not None
        async with self._lock:
            val = self._db[key]
            del self._db[key]
        return val

    async def set_key(self, key, value):
        assert self._db is not None
        async with self._lock:
            self._db[key] = value

    async def set_multiple_keys(self, value_dict):
        assert self._db is not None
        async with self._lock:
            for key, val in value_dict.items:
                self._db[key] = val

    async def del_key(self, key):
        assert self._db is not None
        async with self._lock:
            del self._db[key]

    async def del_all_keys(self):
        assert self._db is not None

        async with self._lock:
            self._db.close()
            self._db = dbm.open(self.db_filename, "n")
