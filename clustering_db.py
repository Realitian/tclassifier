import pymysql
import os
from urllib.parse import urlparse

class ClusteringDB:
    def __init__(self):
        # path = "mysql://be9e7647d58416:04556a3b@us-cdbr-iron-east-01.cleardb.net/heroku_510f19273e88adc?reconnect=true"
        # path = "mysql://root:rootroot@localhost:3306/mokametics"
        path = os.environ['CLEARDB_DATABASE_URL']
        url = urlparse(path)

        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port

        self.db = pymysql.connect(host, user, password, dbname, charset='utf8')

    def closeDB(self):
        cursor = self.db.cursor()
        cursor.close()
        self.db.close()

    def putMessage(self, company_id, time_from, time_to, category, num_clusters):
        sql = """INSERT INTO clustering (company_id, time_from, time_to, category, num_clusters, status) VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor = self.db.cursor()
        cursor.execute(sql, (company_id, time_from, time_to, category, num_clusters, 0))
        self.db.commit()

    def getMessage(self):
        sql = """select id, company_id, time_from, time_to, category, num_clusters from clustering where status = 0 order by id limit 1"""
        cursor = self.db.cursor()
        cursor.execute(sql)
        res = cursor.fetchone()
        return res

    def setMessage(self, id):
        sql = """update clustering set status=%s where id=%s"""
        cursor = self.db.cursor()
        cursor.execute(sql, (1, id))
        self.db.commit()