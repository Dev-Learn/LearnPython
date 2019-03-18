import pymysql
import json
from flask import Flask, request, Response
from flask.json import jsonify

from util.error import ErrorHandler

app = Flask(__name__)


def conn():
    return pymysql.connect(host='localhost',
                           user='root',
                           db='chart_song',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)


@app.route('/getChartMusic')
def getChartMusic():
    connection = conn()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT * FROM week")
        weeks = cursor.fetchall()
        return Response(json.dumps(weeks), mimetype='application/json')
    except Exception as e:
        return error_return(ErrorHandler(str(e), status_code=500))
    finally:
        cursor.close()
        connection.close()


@app.route('/getSongWeek')
def getSongWeek():
    weekId = request.args.get('weekId')
    connection = conn()
    cursor = connection.cursor()
    try:
        datas = []
        cursor.execute(
            "SELECT * FROM week_song WHERE id_week = '%s'" % weekId)
        week_songs = cursor.fetchall()
        for item in week_songs:
            data = {}
            cursor.execute(
                "SELECT * FROM song WHERE id = '%s'" % item['id_song'])
            song = cursor.fetchone()
            cursor.execute(
                "SELECT id_singer FROM singer_song WHERE id_song = '%s'" % song['id'])
            idSinger = cursor.fetchone()
            cursor.execute("SELECT name FROM singer where id = '%s'" % idSinger['id_singer'])
            singer = cursor.fetchone()
            song['singer'] = singer['name']
            data['song'] = song
            data['position'] = item['position']
            data['hierarchical'] = item['hierarchical']
            data['hierarchical_number'] = item['hierarchical_number']
            datas.append(data)
        return Response(json.dumps(datas), mimetype='application/json')
    except Exception as e:
        return error_return(ErrorHandler(str(e), status_code=500))
    finally:
        cursor.close()
        connection.close()


@app.route('/getSinger')
def getSinger():
    connection = conn()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT * FROM singer")
        singers = cursor.fetchall()
        return Response(json.dumps(singers), mimetype='application/json')
    except Exception as e:
        return error_return(ErrorHandler(str(e), status_code=500))
    finally:
        cursor.close()
        connection.close()


@app.route('/getSongSinger')
def getSongSinger():
    singerId = request.args.get('singerId')
    connection = conn()
    cursor = connection.cursor()
    try:
        data = []
        cursor.execute(
            "SELECT name FROM singer WHERE id = '%s'" % singerId)
        singer_name = cursor.fetchone()
        cursor.execute(
            "SELECT id_song FROM singer_song WHERE id_singer = '%s'" % singerId)
        listIdSongs = cursor.fetchall()
        for song in listIdSongs:
            cursor.execute(
                "SELECT * FROM song WHERE id = '%s'" % song['id_song'])
            song = cursor.fetchone()
            song['singer'] = singer_name
            data.append(song)
        return Response(json.dumps(data), mimetype='application/json')
    except Exception as e:
        return error_return(ErrorHandler(str(e), status_code=500))
    finally:
        cursor.close()
        connection.close()


@app.errorhandler(ErrorHandler)
def error_return(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    app.run(host='192.168.1.84', debug=True)

