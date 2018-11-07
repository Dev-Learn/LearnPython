import json
import pymysql
from flask import Flask, request, Response

connection = pymysql.connect(host='localhost',
                             user='root',
                             db='comic',
                             use_unicode=True,
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)


@app.route('/getComic')
def getComic():
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


@app.route('/getComicImage', methods=['POST'])
def getComicImage():
    try:
        requestBody = request.json
        # print(requestBody['id'] + " - " + requestBody['offset'] + " - " + requestBody['count'])
        mycursor = connection.cursor()
        mycursor.execute("SELECT * FROM linkimage WHERE idcomic = %s LIMIT %s,%s" % (
            str(requestBody['id']), str(requestBody['offset']), str(requestBody['count'])))
        return Response(json.dumps({'success': True, 'result': mycursor.fetchall()}), mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({'success': False, 'message': str(e)}), mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)
