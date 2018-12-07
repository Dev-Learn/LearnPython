import json
import pymysql
from requests import HTTPError
from secrets import token_hex
from flask import jsonify
import os

from practice10.main import auth, storage
from flask import Flask, request, Response

from util.error import ErrorHandler

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

INVALID_TOKEN = 401
SERVER_ERROR = 500
BAD_REQUEST = 400
NOT_FOUND = 404
VERIFY_EMAIL = 600

APP_ROOT = os.path.dirname(os.path.abspath(__file__))


def conn():
    return pymysql.connect(host='us-cdbr-iron-east-01.cleardb.net',
                           user='b40fd74efb18c2',
                           password='e2547e43',
                           db='heroku_4a4d86265c8552e',
                           use_unicode=True,
                           charset='utf8',
                           cursorclass=pymysql.cursors.DictCursor)


@app.route('/getComicOffset')
def getComicOffset():
    token = request.headers.get('token')
    offset = request.args.get('offset')
    count = request.args.get('count')

    connection = conn()
    cursor = connection.cursor()

    try:

        if not token:
            return error_return(ErrorHandler('Invalid Request', status_code=BAD_REQUEST))
        if validData(cursor, 'user', 'token', token):
            cursor.execute("SELECT * FROM comic LIMIT %s,%s" % (offset, count))
            comics = cursor.fetchall()
            for comic in comics:
                cursor.execute("SELECT * FROM genre WHERE idcomic = %s" % comic['id'])
                comic['genre'] = cursor.fetchall()
            cursor.close()
            return Response(json.dumps(comics), mimetype='application/json')
        else:
            cursor.close()
            return error_return(ErrorHandler('Invalid Token', status_code=INVALID_TOKEN))
    except Exception as e:
        return error_return(ErrorHandler(str(e), status_code=SERVER_ERROR))
    finally:
        connection.close()
        cursor.close()


@app.route('/getComic')
def getComic():
    token = request.headers.get('token')
    after = request.args.get('after')
    limit = request.args.get('limit')

    connection = conn()
    cursor = connection.cursor()

    try:
        if not token:
            return error_return(ErrorHandler('Invalid Request', status_code=BAD_REQUEST))

        if validData(cursor, 'user', 'token', token):
            if after:
                cursor.execute("SELECT * FROM comic WHERE comic.id > %s LIMIT %s" % (str(after), str(limit)))
            else:
                cursor.execute("SELECT * FROM comic LIMIT %s" % (str(limit)))
            comics = cursor.fetchall()
            for comic in comics:
                cursor.execute("SELECT * FROM genre WHERE idcomic = %s" % comic['id'])
                comic['genre'] = cursor.fetchall()
            return Response(json.dumps(comics), mimetype='application/json')
        else:
            return error_return(ErrorHandler('Invalid Token', status_code=INVALID_TOKEN))
    except Exception as e:
        return error_return(ErrorHandler(str(e), status_code=SERVER_ERROR))
    finally:
        connection.close()
        cursor.close()


@app.route('/getComicImage/<int:id>')
def getComicImage(id):
    token = request.headers.get('token')
    after = request.args.get('after')
    limit = request.args.get('limit')

    connection = conn()
    cursor = connection.cursor()
    try:
        if not token:
            return error_return(ErrorHandler('Invalid Request', status_code=BAD_REQUEST))

        if validData(cursor, 'user', 'token', token):
            if after:
                cursor.execute("SELECT * FROM linkimage WHERE idcomic = %s AND linkimage.id > %s LIMIT %s" % (
                    str(id), after, limit))
            else:
                cursor.execute("SELECT * FROM linkimage WHERE idcomic = %s LIMIT %s" % (
                    str(id), limit))

            data = cursor.fetchall()
            return Response(json.dumps(data), mimetype='application/json')
        else:
            return error_return(ErrorHandler('Invalid Token', status_code=INVALID_TOKEN))
    except Exception as e:
        return error_return(ErrorHandler(str(e), status_code=SERVER_ERROR))
    finally:
        connection.close()
        cursor.close()


@app.route('/register', methods=['PUT'])
def register():
    data = request.json
    connection = conn()
    cursor = connection.cursor()
    try:
        user = auth.create_user_with_email_and_password(data['email'], data['password'])
        auth.send_email_verification(user['idToken'])
        sql = "INSERT INTO `user` (name, email, token_firebase, token) VALUES (%s, %s, %s, %s)"
        val = (data['name'], data['email'], user['idToken'], '')
        cursor.execute(sql, val)
        connection.commit()
        return Response(json.dumps('Please verify email !!!'), mimetype='application/json')
    except HTTPError as e:
        response = e.args[0].response
        error = response.json()['error']['message']
        return error_return(ErrorHandler(error, status_code=SERVER_ERROR))
    finally:
        connection.close()
        cursor.close()


@app.route('/login', methods=['POST'])
def login():
    data = request.json

    connection = conn()
    cursor = connection.cursor()

    try:
        user = auth.sign_in_with_email_and_password(data['email'], data['password'])
        token_firebase = user['idToken']
        print(token_firebase)
        info = auth.get_account_info(token_firebase)
        user = info['users'][0]
        if user['emailVerified']:
            cursor.execute(
                "SELECT user.id FROM user WHERE email = %s",
                (data['email'],)
            )
            id = cursor.fetchone()['id']
            if id:
                utoken = token_hex(32)
                sql = "UPDATE user SET token = %s WHERE id = %s"
                val = (utoken, str(id))
                cursor.execute(sql, val)
                connection.commit()
                return Response(json.dumps(utoken), mimetype='application/json')
            else:
                return error_return(ErrorHandler('User Not Found', status_code=NOT_FOUND))
        else:
            return error_return(ErrorHandler('Email not verify !!!', status_code=VERIFY_EMAIL))
    except HTTPError as e:
        response = e.args[0].response
        error = response.json()['error']['message']
        return error_return(ErrorHandler(error, status_code=SERVER_ERROR))
    finally:
        connection.close()
        cursor.close()


@app.route('/resetPassword', methods=['POST'])
def resetPassword():
    try:
        data = request.json
        auth.send_password_reset_email(data['email'])
        return Response(json.dumps('Please check email !!!'), mimetype='application/json')
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
        user = auth.sign_in_with_email_and_password(data['email'], data['password'])
        auth.send_email_verification(user['idToken'])
        return Response()
    except HTTPError as e:
        response = e.args[0].response
        error = response.json()['error']['message']
        return error_return(ErrorHandler(error, status_code=SERVER_ERROR))
    except Exception as e:
        return error_return(ErrorHandler(str(e), status_code=SERVER_ERROR))


@app.route('/userInfo', methods=['POST'])
def userInfo():
    token = request.headers.get('token')
    connection = conn()
    cursor = connection.cursor()

    try:

        if not token:
            return error_return(ErrorHandler('Invalid Request', status_code=BAD_REQUEST))

        if validData(cursor, 'user', 'token', token):
            cursor.execute(
                "SELECT tbUser.id,tbUser.name,tbUser.email,(SELECT link FROM picture WHERE id_user = tbUser.id) as avarta FROM user AS tbUser WHERE token = %s",
                token
            )
            data = cursor.fetchone()
            return Response(json.dumps(data), mimetype='application/json')
        else:
            return error_return(ErrorHandler('Invalid Token', status_code=INVALID_TOKEN))
    except Exception as e:
        return error_return(ErrorHandler(str(e), status_code=SERVER_ERROR))
    finally:
        connection.close()
        cursor.close()


@app.route('/updateInfo', methods=['POST'])
def updateInfo():
    token = request.headers.get('token')
    connection = conn()
    cursor = connection.cursor()
    try:
        id = request.form.get('id')
        name = request.form.get('name')
        avarta = request.files['picture']

        if not token or not id or not name:
            return error_return(ErrorHandler('Invalid Request', status_code=BAD_REQUEST))

        if validData(cursor, 'user', 'token', token):
            if validData(cursor, 'user', 'id', id):
                sql = "UPDATE `user` SET `name` = %s WHERE id = %s"
                val = [name, id]

                target = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'avarta')
                print(target)

                if not os.path.isdir(target):
                    os.mkdir(target)

                cursor.execute(
                    "SELECT token_firebase FROM user WHERE id = '%s'" % id
                )
                token = cursor.fetchone()['token_firebase']

                url = "images/%s" % id
                storage.child(url).put(avarta, token)

                if validData(cursor, 'picture', 'id_user', id):
                    sql2 = "UPDATE `picture` SET `link` = %s WHERE id_user = %s"
                    val2 = [storage.child(url).get_url(token), id]
                else:
                    sql2 = "INSERT INTO `picture` (id_user, link) VALUES (%s, %s)"
                    val2 = [id, storage.child(url).get_url(token)]

                cursor.execute(sql, val)
                cursor.execute(sql2, val2)
                connection.commit()
                return Response()
            else:
                return error_return(ErrorHandler('Not found User', status_code=BAD_REQUEST))
        else:
            return error_return(ErrorHandler('Invalid Token', status_code=INVALID_TOKEN))
    except Exception as e:
        return error_return(ErrorHandler(str(e), status_code=SERVER_ERROR))
    finally:
        connection.close()
        cursor.close()


@app.route('/getArticle')
def getArticle():
    after = request.args.get('after')
    before = request.args.get('before')
    limit = request.args.get('limit')

    token = request.headers.get('token')

    connection = conn()
    cursor = connection.cursor()

    try:

        if not token:
            return error_return(ErrorHandler('Invalid Request', status_code=BAD_REQUEST))

        if validData(cursor, 'user', 'token', token):

            if before:
                after_ = int(before) - int(limit)
                cursor.execute(
                    "SELECT * FROM article WHERE id < %s AND id > %s  LIMIT %s" % (
                        str(before), str(after_), str(limit)))
            elif after:
                cursor.execute("SELECT * FROM article WHERE id > %s LIMIT %s" % (str(after), str(limit)))
            else:
                cursor.execute("SELECT * FROM article LIMIT %s" % str(limit))
            articles = cursor.fetchall()
            for item in articles:
                cursor.execute("SELECT * FROM author WHERE id = %s" % item['id_author'])
                author = cursor.fetchone()
                item['author'] = author

                cursor.execute("SELECT * FROM article_detail WHERE id = %s" % item['id_detail'])
                detail = cursor.fetchone()
                item['detail'] = detail

            return Response(json.dumps(articles), mimetype='application/json')
        else:
            return error_return(ErrorHandler('Invalid Token', status_code=INVALID_TOKEN))
    except Exception as e:
        return error_return(ErrorHandler(str(e), status_code=SERVER_ERROR))
    finally:
        connection.close()
        cursor.close()


def validData(cursor, table, field, value):
    cursor.execute(
        "SELECT COUNT(*) FROM %s WHERE %s = '%s'" % (table, field, value)
    )
    count = cursor.fetchone()
    return count['COUNT(*)'] == 1


@app.errorhandler(ErrorHandler)
def error_return(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


if __name__ == '__main__':
    app.run()
