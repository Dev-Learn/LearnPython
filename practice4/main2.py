import json

import pymysql
from flask import Flask, Response
from flask.json import jsonify

from util.error import ErrorHandler

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def conn():
    return pymysql.connect(host='localhost',
                           user='root',
                           db='toiec',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)


@app.route('/getTopic')
def getTopic():
    connection = conn()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT * FROM topic")
        topics = cursor.fetchall()
        return Response(json.dumps(topics), mimetype='application/json')
    except Exception as e:
        return error_return(ErrorHandler(str(e), status_code=500))
    finally:
        cursor.close()
        connection.close()


@app.route('/getWord')
def getWord():
    connection = conn()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT * FROM word")
        words = cursor.fetchall()
        return Response(json.dumps(words), mimetype='application/json')
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
