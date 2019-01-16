import psycopg2
import urlparse
import os

class DailyDB:
    def __init__(self):
        #test url : "postgres://postgres:postgres@localhost:5432/mokadaily_development"
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        # url = urlparse.urlparse("postgres://postgres:postgres@localhost:5432/mokadaily_development")
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port

        self.db = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)

        print ('connection to db had success')

        sql = """select * from investors limit 1"""
        cursor = self.db.cursor()
        cursor.execute(sql)
        res = cursor.fetchall()
        print (res)


    def closeDB(self):
        cursor = self.db.cursor()
        cursor.close()
        self.db.close()

    def set_catescore(self, id, catescore, label):
        sql = """update investors set catescore=%s, catelabel=%s where id=%s"""
        cursor = self.db.cursor()
        cursor.execute(sql, (catescore, label, id))
        self.db.commit()

    def get_todo_count(self):
        sql = """select count(id) from investors where company and catescore is null"""
        cursor = self.db.cursor()
        cursor.execute(sql)
        res = cursor.fetchone()
        return res[0]

    def get_todo_list(self, offset):
        sql = """select id, content from investors where company and catescore is null limit 1000 offset %s"""
        cursor = self.db.cursor()
        cursor.execute(sql, (offset,))
        res = cursor.fetchall()
        return res

    def select_tweets(self, company_id, time_from, time_to, category):
        sql = """select id, content from investors where id in (select investor_id from companies_investors where company_id=%s) and created_at BETWEEN %s AND %s and catelabel=%s"""
        cursor = self.db.cursor()
        cursor.execute(sql, (company_id, time_from, time_to, category))
        res = cursor.fetchall()
        return res

    def set_tweet_clusterid(self, id, clusterid):
        sql = """update investors set clusterid=%s where id=%s"""
        cursor = self.db.cursor()
        cursor.execute(sql, (clusterid, id))
        self.db.commit()

    def set_tweet_clusterids(self, clusterids):
        sql = """update investors set clusterid=%s where id=%s"""
        cursor = self.db.cursor()
        cursor.executemany(sql, clusterids)
        self.db.commit()