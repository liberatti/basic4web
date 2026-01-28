import json

import redis


class RedisDAO:
    def __init__(self, host="127.0.0.1", port=6379, password=None, conn=None, db=0):
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.conn = conn

    def connect(self):
        if not self.conn:
            self.conn = redis.Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                db=self.db,
                decode_responses=True
            )

    def is_connected(self):
        try:
            return self.conn and self.conn.ping()
        except (redis.ConnectionError, AttributeError):
            return False

    def persist(self, k, v, expire=None):
        if expire:
            self.conn.set(k, v, ex=expire)
        else:
            self.conn.set(k, v)

    def get_by_id(self, k):
        return self.conn.get(k)

    def delete(self, k):
        self.conn.delete(k)

    def get_keys_by_prefix(self, pattern="*"):
        return list(self.conn.scan_iter(match=pattern))

    def get_items_by_prefix(self, pattern="*"):
        items = list()
        for key in self.conn.scan_iter(match=pattern):
            j = self.conn.get(key)
            i = json.loads(j)
            i.update({"_id": key})
            items.append(i)
        return items

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
