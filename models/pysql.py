import pymysql, os

class pysql:
    def __init__(self):
        senha = os.getenv("AIVEN_PASSWORD")
        self.config = {
            "host": "mysql-jetmoney.k.aivencloud.com",
            "user": "avnadmin",
            "password": senha,
            "db": "dbjetmoney",
            "port": 14013,
            "ssl": {"ssl-mode": "REQUIRED"},
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