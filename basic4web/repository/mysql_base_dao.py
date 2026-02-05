import pymysql
from marshmallow import Schema, fields

from basic4web.middleware.logging import logger
from basic4web.repository.schemas.page_meta_schema import PageMetaSchema


class MySQLDAO:

    def __init__(
            self, host, port, user, password, database, table_name, schema=None, conn=None
    ):
        self.table_name = table_name
        self.schema = schema() if schema else None
        self.pageSchema = None
        self.conn = (
            conn
            if conn
            else pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port,
                cursorclass=pymysql.cursors.DictCursor,
                connect_timeout=300,
                autocommit=True,
            )
        )

        if schema:
            page_class = type(
                "pagination",
                (Schema,),
                {
                    "metadata": fields.Nested(PageMetaSchema, many=False),
                    "data": fields.Nested(schema, many=True),
                },
            )
            self.pageSchema = page_class()

    def to_dict(self, row):
        return row

    def from_dict(self, row):
        return row

    def json_load(self, json_data, many=False):
        return self.schema.load(json_data, many=many) if self.schema else json_data

    def json_dump(self, row, many=False):
        return self.schema.dump(row, many=many) if self.schema else row

    def _interpolate_sql(self, sql, params):
        if not params:
            return sql
        try:
            escaped = tuple(repr(p) for p in params)
            return sql % escaped
        except Exception:
            return f"{sql} | PARAMS: {params}"

    def _query(self, sql, params=None, fetch=False):
        cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        logger.debug(self._interpolate_sql(sql, params))
        try:
            cursor.execute(sql, params)
            if fetch:
                return cursor.fetchall()
        finally:
            cursor.close()

    def __del__(self):
        self.conn.close()

    def get_all(self, pagination=None, order_by=None):
        sql = f"SELECT * FROM {self.table_name}"
        if order_by:
            sql += f" order by {order_by}"
        count_sql = f"SELECT COUNT(*) AS total FROM {self.table_name}"
        rows = []
        total = self._query(count_sql, fetch=True)[0]["total"]

        if pagination:
            page = pagination.get("page", 1)
            per_page = pagination.get("per_page", 10)
            offset = (page - 1) * per_page
            sql += f" LIMIT {per_page} OFFSET {offset}"
            pagination["total_elements"] = total
        else:
            pagination = {"total_elements": total, "page": 1, "per_page": total}

        rs = self._query(sql, fetch=True)
        if rs:
            rows = [row for row in rs]
            for r in rows:
                self.to_dict(r)
        return {
            "metadata": pagination,
            "data": rows,
        }

    def get_desc_by_id(self, id):
        sql = f"SELECT id,name FROM {self.table_name} WHERE id = %s"
        rs = self._query(sql, (id,), fetch=True)
        row = rs[0] if rs else None
        self.to_dict(row)
        return row

    def get_by_id(self, id):
        sql = f"SELECT * FROM {self.table_name} WHERE id = %s"
        rs = self._query(sql, (id,), fetch=True)
        row = rs[0] if rs else None
        self.to_dict(row)
        return row

    def get_by_name(self, name):
        sql = f"SELECT * FROM {self.table_name} WHERE name = %s LIMIT 1"
        rs = self._query(sql, (name,), fetch=True)
        row = rs[0] if rs else None
        self.to_dict(row)
        return row

    def update_by_id(self, id, vo):
        self.from_dict(vo)
        keys = ", ".join([f"{k} = %s" for k in vo.keys()])
        sql = f"UPDATE {self.table_name} SET {keys} WHERE id = %s"
        values = list(vo.values()) + [id]
        self._query(sql, values)
        self.conn.commit()
        return True

    def persist(self, vo):
        self.from_dict(vo)
        keys = ", ".join(vo.keys())
        values_placeholder = ", ".join(["%s"] * len(vo))
        sql = f"INSERT INTO {self.table_name} ({keys}) VALUES ({values_placeholder})"
        values = list(vo.values())

        cursor = self.conn.cursor()
        try:
            logger.debug(self._interpolate_sql(sql, values))
            cursor.execute(sql, values)
            self.conn.commit()
            return cursor.lastrowid
        finally:
            cursor.close()

    def persist_many(self, arr):
        if not arr:
            return False
        keys = ", ".join(arr[0].keys())
        values_placeholder = ", ".join(["%s"] * len(arr[0]))
        sql = f"INSERT INTO {self.table_name} ({keys}) VALUES ({values_placeholder})"
        for item in arr:
            self._query(sql, tuple(item.values()))
        self.conn.commit()
        return True

    def delete_by_id(self, id):
        sql = f"DELETE FROM {self.table_name} WHERE id = %s"
        self._query(sql, (id,))
        return True

    def delete_all(self):
        sql = f"DELETE FROM {self.table_name}"
        self._query(sql)
        return True

    def count_all(self, where_clause=None, params=None):
        """
        Count all records in the table with optional where clause

        Args:
            where_clause (str, optional): SQL WHERE clause. Defaults to None.
            params (tuple, optional): Parameters for the WHERE clause. Defaults to None.

        Returns:
            int: Total count of records
        """
        sql = f"SELECT COUNT(*) AS total FROM {self.table_name}"
        if where_clause:
            sql += f" WHERE {where_clause}"
        logger.debug(sql)
        result = self._query(sql, params, fetch=True)
        return result[0]["total"] if result else 0
