import pymysql
from practice10.main import storage

def conn():
    return pymysql.connect(host='localhost',
                           user='root',
                           db='chart_song',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)


if __name__ == '__main__':
    connection = conn()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM song")
    listSong = cursor.fetchall()
    for item in listSong:
        token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjIzNTBiNWY2NDM0Zjc2Y2NiM2IxMTlmZGQ4OGQxMzhjOWFjNTVmY2UiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vbGVhcm5weXRob24tODhjM2YiLCJhdWQiOiJsZWFybnB5dGhvbi04OGMzZiIsImF1dGhfdGltZSI6MTU0MzYzNTU1OCwidXNlcl9p"
        url = "managerThread/%s" % item['name']
        storage.child(url).put(item['link_local'], token)
        link = storage.child(url).get_url(token)
        print(link)
        sql = "UPDATE song SET link_local = %s where id = %s"
        val = [link, item['id']]
        cursor.execute(sql, val)
        connection.commit()