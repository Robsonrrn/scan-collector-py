import sqlite3
from sqlite3 import Error


class CookiesRepository:

    def __init__(self, dbDirFile):
        self.dbDirFile = dbDirFile

    def getCookiesByDomainId(self):
        conn = None
        try:
            conn = sqlite3.connect(self.dbDirFile)
            print("PATH DB COOKIES: " + self.dbDirFile)
            c = conn.cursor()
            c.execute('select * from cookies')
            print("Curso OK")
            result = c.fetchall()
            print(result)
            return result
        except Error as e:
            print(e)
        finally:
            if conn:
                conn.close()
