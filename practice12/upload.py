import pymysql
from practice10.main import storage
import requests
import os
import dropbox

client = dropbox.Dropbox("ut9MzqycHAAAAAAAAAAAM-HAvZ8JWgqcOSvr5e3VdjJnlPoTByUGs11BUsUzFl1T")


def conn():
    return pymysql.connect(host='us-cdbr-iron-east-03.cleardb.net',
                           user='bbc01008ee8dff',
                           password='7c06ebdf',
                           db='heroku_aa2646e5ac763f9',
                           use_unicode=True,
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)


if __name__ == '__main__':
    connection = conn()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM song")
    listSong = cursor.fetchall()
    for item in listSong:
        token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjIzNTBiNWY2NDM0Zjc2Y2NiM2IxMTlmZGQ4OGQxMzhjOWFjNTVmY2UiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vbGVhcm5weXRob24tODhjM2YiLCJhdWQiOiJsZWFybnB5dGhvbi04OGMzZiIsImF1dGhfdGltZSI6MTU0MzYzNTU1OCwidXNlcl9p"
        # url = "managerThread/%s" % item['name']
        # storage.child(url).put(item['link_local'], token)
        # link = storage.child(url).get_url(token)
        # print(link)
        # sql = "UPDATE song SET link_local = %s where id = %s"
        # val = [link, item['id']]
        # cursor.execute(sql, val)
        # connection.commit()
        target = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'music')
        print(target)

        if not os.path.isdir(target):
            os.mkdir(target)
        name = item['name'] + ".mp3"
        target = target + "/" + name
        link = item['link_local']
        print(link)
        r = requests.get(link)
        client.files_upload(r.content, "/" + name)
        print(client.files_get_metadata("/" + name))
        sql = "UPDATE song SET link_local = %s where id = %s"
        val = ["/" + name, item['id']]
        cursor.execute(sql, val)
        connection.commit()
