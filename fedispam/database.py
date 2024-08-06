from asyncio import Lock


class Database:
    def __init__(self, db_file):
        self._lock = Lock
    
    def close(self):
        # TODO


class ModelDatabase(Database): ...


class OutliarDatabase(Database): ...


class PreprocessedMessages(Database): ...
