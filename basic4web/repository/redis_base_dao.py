import json
import redis


class RedisDAO:
    def __init__(self, host="127.0.0.1", port=6379, password=None, db=0):
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.conn = None

    def connect(self):
        if not self.conn:
            self.conn = redis.Redis(
                host=self.host,
                port=self.port,
                password=self.password,
                db=self.db,
                decode_responses=True,
            )
            self.conn.ping()

    def _ensure_connection(self):
        if not self.is_connected():
            self.connect()

    def is_connected(self):
        try:
            return self.conn and self.conn.ping()
        except (redis.ConnectionError, AttributeError):
            return False

    def persist(self, key, value, expire=None):
        self._ensure_connection()
        payload = json.dumps(value)
        self.conn.set(key, payload, ex=expire)

    def get_by_id(self, key):
        self._ensure_connection()
        value = self.conn.get(key)
        return json.loads(value) if value else None

    def delete(self, key):
        self._ensure_connection()
        return self.conn.delete(key)

    def get_keys_by_prefix(self, pattern="*"):
        self._ensure_connection()
        return list(self.conn.scan_iter(match=pattern))

    def get_items_by_prefix(self, pattern="*"):
        items = []

        for key in self.conn.scan_iter(match=pattern):
            raw = self.conn.get(key)
            if not raw:
                continue

            try:
                data = json.loads(raw)
                if isinstance(data, dict):
                    data["_id"] = key
                else:
                    data = {"_id": key, "value": data}
                items.append(data)
            except (json.JSONDecodeError, TypeError):
                continue

        return items

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()
