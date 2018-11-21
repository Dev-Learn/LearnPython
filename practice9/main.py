import json
import pymysql
import pyrebase
from flask import Flask, request, Response

connection = pymysql.connect(host='localhost',
                             user='root',
                             db='comic',
                             use_unicode=True,
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)




@app.route('/getComicOffset')
def getComicOffset():
    try:
        offset = request.args.get('offset')
        count = request.args.get('count')
        mycursor = connection.cursor()
        mycursor.execute("SELECT * FROM comic LIMIT %s,%s" % (offset, count))
        comics = mycursor.fetchall()
        for comic in comics:
            mycursor.execute("SELECT * FROM genre WHERE idcomic = %s" % comic['id'])
            comic['genre'] = mycursor.fetchall()
        return Response(json.dumps({'success': True, 'result': comics}), mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({'success': False, 'message': str(e)}), mimetype='application/json')


@app.route('/getComic')
def getComic():
    try:
        after = request.args.get('after')
        limit = request.args.get('limit')
        mycursor = connection.cursor()
        if after:
            mycursor.execute("SELECT * FROM comic WHERE comic.id > %s LIMIT %s" % (str(after), str(limit)))
        else:
            mycursor.execute("SELECT * FROM comic LIMIT %s" % (str(limit)))
        comics = mycursor.fetchall()
        for comic in comics:
            mycursor.execute("SELECT * FROM genre WHERE idcomic = %s" % comic['id'])
            comic['genre'] = mycursor.fetchall()
        return Response(json.dumps({'success': True, 'result': comics}), mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({'success': False, 'message': str(e)}), mimetype='application/json')


@app.route('/getComicImage/<int:id>')
def getComicImage(id):
    try:
        after = request.args.get('after')
        limit = request.args.get('limit')
        # idComic = request.json
        # print(requestBody['id'] + " - " + requestBody['offset'] + " - " + requestBody['count'])
        mycursor = connection.cursor()

        if after:
            mycursor.execute("SELECT * FROM linkimage WHERE idcomic = %s AND linkimage.id > %s LIMIT %s" % (
                str(id), after, limit))
        else:
            mycursor.execute("SELECT * FROM linkimage WHERE idcomic = %s LIMIT %s" % (
                str(id), limit))

        data = mycursor.fetchall()
        mycursor.close()
        return Response(json.dumps({'success': True, 'result': data}), mimetype='application/json')
    except Exception as e:

        return Response(json.dumps({'success': False, 'message': str(e)}), mimetype='application/json')


if __name__ == '__main__':
    app.run(host="192.168.7.152", debug=True)
