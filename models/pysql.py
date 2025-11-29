import pymysql

class pysql:
    def __init__(self):
        self.config = {
            "host": "localhost",
            "user": "root",
            "password": "",
            "db": "dbjetmoney",
            "charset": "utf8",
            "use_unicode": True
        }

    def execute(self, sql, params=None):
        conn = pymysql.connect(**self.config)  # desempacota o dicionario
        cur = conn.cursor()
        try:
            cur.execute(sql, params)
            conn.commit()
            return cur.rowcount
        except pymysql.Error as erro:
            raise erro
        finally:
            cur.close()
            conn.close()

    def search(self, sql, params=None, one=False):
        conn = pymysql.connect(**self.config)
        cur = conn.cursor()
        try:
            cur.execute(sql, params)
            return cur.fetchone() if one else cur.fetchall()
        except pymysql.Error as erro:
            raise erro
        finally:
            cur.close()
            conn.close()