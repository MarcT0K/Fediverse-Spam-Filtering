import dbm

from asyncio import Lock
from typing import Dict, List, Union

DB_ENTRY_TYPE = Union[str, bytes]


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

    async def get_all_keys(self) -> List[bytes]:
        assert self._db is not None
        async with self._lock:
            keys = self._db.keys()
        return keys

    async def get_all_key_values(self) -> Dict[bytes, bytes]:
        assert self._db is not None
        async with self._lock:
            db_dict = {key: self._db[key] for key in self._db.keys()}
        return db_dict

    async def get_key(self, key: DB_ENTRY_TYPE) -> bytes:
        assert self._db is not None
        async with self._lock:
            val = self._db[key]
        return val

    async def get_and_del_key(self, key: DB_ENTRY_TYPE) -> bytes:
        assert self._db is not None
        async with self._lock:
            val = self._db[key]
            del self._db[key]
        return val

    async def set_key(self, key: DB_ENTRY_TYPE, value: DB_ENTRY_TYPE) -> None:
        assert self._db is not None
        async with self._lock:
            self._db[key] = value

    async def set_multiple_keys(
        self, value_dict: Dict[DB_ENTRY_TYPE, DB_ENTRY_TYPE]
    ) -> None:
        assert self._db is not None
        async with self._lock:
            for key, val in value_dict.items():
                self._db[key] = val

    async def del_key(self, key) -> None:
        assert self._db is not None
        async with self._lock:
            del self._db[key]

    async def del_all_keys(self) -> None:
        assert self._db is not None

        async with self._lock:
            self._db.close()
            self._db = dbm.open(self.db_filename, "n")
