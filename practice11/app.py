import json

import pymysql
from flask import Flask, request, Response

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def conn():
    return pymysql.connect(host='localhost',
                           user='root',
                           db='tinhte',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)


@app.route('/getArticle')
def getArticle():
    after = request.args.get('after')
    before = request.args.get('before')
    limit = request.args.get('limit')

    connection = conn()
    cursor = connection.cursor()

    if before:
        cursor.execute(
            "SELECT * FROM article WHERE id < %s ORDER BY id DESC LIMIT %s" % (str(before), str(limit)))
    elif after:
        cursor.execute("SELECT * FROM article WHERE article.id > %s LIMIT %s" % (str(after), str(limit)))
    else:
        cursor.execute("SELECT * FROM article LIMIT %s" % str(limit))
    articles = cursor.fetchall()
    if before and articles:
        articles.reverse()
    for item in articles:
        cursor.execute("SELECT * FROM author WHERE id = %s" % item['id_author'])
        author = cursor.fetchone()
        item['author'] = author

        cursor.execute("SELECT * FROM article_detail WHERE id = %s" % item['id_detail'])
        detail = cursor.fetchone()
        item['detail'] = detail

    return Response(json.dumps(articles), mimetype='application/json')


if __name__ == '__main__':
    app.run(host='192.168.1.84', debug=True)
