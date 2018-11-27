import json
import pymysql
from requests import HTTPError
from secrets import token_hex
from flask import jsonify

from practice10.main import auth
from flask import Flask, request, Response

from util.error import ErrorHandler

connection = pymysql.connect(host='us-cdbr-iron-east-01.cleardb.net',
                             user='b40fd74efb18c2',
                             password='e2547e43',
                             db='heroku_4a4d86265c8552e',
                             use_unicode=True,
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)

INVALID_TOKEN = 401
SERVER_ERROR = 500
BAD_REQUEST = 400
NOT_FOUND = 404
VERIFY_EMAIL = 600


@app.route('/getComicOffset')
def getComicOffset():
    try:
        token = request.headers.get('token')
        offset = request.args.get('offset')
        count = request.args.get('count')
        if not token:
            return error_return(ErrorHandler('Invalid Request', status_code=BAD_REQUEST))
        mycursor = connection.cursor()
        if validToken(mycursor, token):
            mycursor.execute("SELECT * FROM comic LIMIT %s,%s" % (offset, count))
            comics = mycursor.fetchall()
            for comic in comics:
                mycursor.execute("SELECT * FROM genre WHERE idcomic = %s" % comic['id'])
                comic['genre'] = mycursor.fetchall()
            mycursor.close()
            return Response(json.dumps(comics), mimetype='application/json')
        else:
            mycursor.close()
            return error_return(ErrorHandler('Invalid Token', status_code=INVALID_TOKEN))
    except Exception as e:
        return error_return(ErrorHandler(str(e), status_code=SERVER_ERROR))


@app.route('/getComic')
def getComic():
    try:
        token = request.headers.get('token')
        after = request.args.get('after')
        limit = request.args.get('limit')
        if not token:
            return error_return(ErrorHandler('Invalid Request', status_code=BAD_REQUEST))
        mycursor = connection.cursor()
        if validToken(mycursor, token):
            if after:
                mycursor.execute("SELECT * FROM comic WHERE comic.id > %s LIMIT %s" % (str(after), str(limit)))
            else:
                mycursor.execute("SELECT * FROM comic LIMIT %s" % (str(limit)))
            comics = mycursor.fetchall()
            for comic in comics:
                mycursor.execute("SELECT * FROM genre WHERE idcomic = %s" % comic['id'])
                comic['genre'] = mycursor.fetchall()
            mycursor.close()
            return Response(json.dumps(comics), mimetype='application/json')
        else:
            mycursor.close()
            return error_return(ErrorHandler('Invalid Token', status_code=INVALID_TOKEN))
    except Exception as e:
        return error_return(ErrorHandler(str(e), status_code=SERVER_ERROR))


@app.route('/getComicImage/<int:id>')
def getComicImage(id):
    try:
        token = request.headers.get('token')
        after = request.args.get('after')
        limit = request.args.get('limit')
        # idComic = request.json
        # print(requestBody['id'] + " - " + requestBody['offset'] + " - " + requestBody['count'])
        if not token:
            return error_return(ErrorHandler('Invalid Request', status_code=BAD_REQUEST))
        mycursor = connection.cursor()
        if validToken(mycursor, token):
            if after:
                mycursor.execute("SELECT * FROM linkimage WHERE idcomic = %s AND linkimage.id > %s LIMIT %s" % (
                    str(id), after, limit))
            else:
                mycursor.execute("SELECT * FROM linkimage WHERE idcomic = %s LIMIT %s" % (
                    str(id), limit))

            data = mycursor.fetchall()
            mycursor.close()
            return Response(json.dumps(data), mimetype='application/json')
        else:
            mycursor.close()
            return error_return(ErrorHandler('Invalid Token', status_code=INVALID_TOKEN))
    except Exception as e:
        return error_return(ErrorHandler(str(e), status_code=SERVER_ERROR))


@app.route('/register', methods=['PUT'])
def register():
    data = request.json
    print(data['name'])
    print(data['email'])
    print(data['password'])
    try:
        user = auth.create_user_with_email_and_password(data['email'], data['password'])
        auth.send_email_verification(user['idToken'])
        mycursor = connection.cursor()
        sql = "INSERT INTO `user` (name, email, token_firebase, token) VALUES (%s, %s, %s, %s)"
        val = (data['name'], data['email'], user['idToken'], '')
        mycursor.execute(sql, val)
        connection.commit()
        mycursor.close()
        return Response(json.dumps('Please verify email !!!'))
    except HTTPError as e:
        response = e.args[0].response
        error = response.json()['error']['message']
        return error_return(ErrorHandler(error, status_code=SERVER_ERROR))


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    print(data['email'])
    print(data['password'])
    try:
        user = auth.sign_in_with_email_and_password(data['email'], data['password'])
        token_firebase = user['idToken']
        print(token_firebase)
        info = auth.get_account_info(token_firebase)
        user = info['users'][0]
        if user['emailVerified']:
            mycursor = connection.cursor()
            mycursor.execute(
                "SELECT user.id FROM user WHERE email = %s",
                (data['email'],)
            )
            id = mycursor.fetchone()['id']
            if id:
                utoken = token_hex(32)
                sql = "UPDATE user SET token = %s WHERE id = %s"
                val = (utoken, str(id))
                mycursor.execute(sql, val)
                connection.commit()
                mycursor.close()
                return Response(json.dumps(utoken), mimetype='application/json')
            else:
                mycursor.close()
                return error_return(ErrorHandler('User Not Found', status_code=NOT_FOUND))
        else:
            return error_return(ErrorHandler('Email not verify !!!', status_code=VERIFY_EMAIL))
    except HTTPError as e:
        response = e.args[0].response
        error = response.json()['error']['message']
        return error_return(ErrorHandler(error, status_code=SERVER_ERROR))


@app.route('/resetPassword', methods=['POST'])
def resetPassword():
    try:
        data = request.json
        print(data)
        auth.send_password_reset_email(data)
        return Response(json.dumps('Please check email !!!'))
    except HTTPError as e:
        response = e.args[0].response
        error = response.json()['error']['message']
        return error_return(ErrorHandler(error, status_code=SERVER_ERROR))
    except Exception as e:
        return error_return(ErrorHandler(str(e), status_code=SERVER_ERROR))


@app.route('/sendEmailVerify', methods=['POST'])
def sendEmailVerify():
    try:
        data = request.json
        print(data['email'])
        print(data['password'])
        user = auth.sign_in_with_email_and_password(data['email'], data['password'])
        auth.send_email_verification(user['idToken'])
        return Response()
    except HTTPError as e:
        response = e.args[0].response
        error = response.json()['error']['message']
        return error_return(ErrorHandler(error, status_code=SERVER_ERROR))
    except Exception as e:
        return error_return(ErrorHandler(str(e), status_code=SERVER_ERROR))


def validToken(cursor, token):
    cursor.execute(
        "SELECT COUNT(*) FROM user WHERE token = %s",
        token
    )
    count = cursor.fetchone()
    return count['COUNT(*)'] == 1


@app.errorhandler(ErrorHandler)
def error_return(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    app.run(host='192.168.7.152', debug=True)
