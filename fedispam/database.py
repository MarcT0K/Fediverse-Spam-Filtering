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

    async def get_key(self, key):
        assert self._db is not None
        async with self._lock:
            val = self._db[key]
        return val

    async def get_all_key_values(self):
        assert self._db is not None
        async with self._lock:
            db_dict = dict(list(self._db.items()))
        return db_dict

    async def set_key(self, key, value):
        assert self._db is not None
        async with self._lock:
            self._db[key] = value

    async def del_key(self, key):
        assert self._db is not None
        async with self._lock:
            del self._db[key]

    async def del_all_keys(self):
        assert self._db is not None

        async with self._lock:
            self._db.close()
            self._db = dbm.open(self.db_filename, "n")
