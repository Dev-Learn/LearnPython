from __future__ import absolute_import

import json

import pymysql
from flask import Flask, Response
from flask.json import jsonify


class ErrorHandler(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


app = Flask(__name__)


def conn():
    return pymysql.connect(host='localhost',
                           user='root',
                           db='toeic_test',
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)


@app.errorhandler(ErrorHandler)
def error_return(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/getTopicType')
def getTopicType():
    connection = conn()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT * FROM topictype")
        topicTypes = cursor.fetchall()
        return Response(json.dumps(topicTypes), mimetype='application/json')
    except Exception as e:
        return error_return(ErrorHandler(str(e), status_code=500))
    finally:
        cursor.close()
        connection.close()


@app.route('/getQuestion')
def getQuestion():
    connection = conn()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT * FROM question")
        questions = cursor.fetchall()
        return Response(json.dumps(questions), mimetype='application/json')
    except Exception as e:
        return error_return(ErrorHandler(str(e), status_code=500))
    finally:
        cursor.close()
        connection.close()


@app.route('/getQuestionChild')
def getQuestionChild():
    connection = conn()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT * FROM questionchild")
        questionchilds = cursor.fetchall()
        return Response(json.dumps(questionchilds), mimetype='application/json')
    except Exception as e:
        return error_return(ErrorHandler(str(e), status_code=500))
    finally:
        cursor.close()
        connection.close()


@app.route('/getAnswer')
def getAnswer():
    connection = conn()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT * FROM answer")
        answers = cursor.fetchall()
        return Response(json.dumps(answers), mimetype='application/json')
    except Exception as e:
        return error_return(ErrorHandler(str(e), status_code=500))
    finally:
        cursor.close()
        connection.close()


@app.route('/getAnswerQuestion')
def getAnswerQuestion():
    connection = conn()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT * FROM answerquestion")
        answerquestions = cursor.fetchall()
        return Response(json.dumps(answerquestions), mimetype='application/json')
    except Exception as e:
        return error_return(ErrorHandler(str(e), status_code=500))
    finally:
        cursor.close()
        connection.close()


if __name__ == '__main__':
    app.debug = True
    app.run()
#     --host 192.168.1.84 --port 5000 => set into additional option
