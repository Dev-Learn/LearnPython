import json
import pymysql
from requests import HTTPError
from secrets import token_hex

from practice10.main import auth
from flask import Flask, request, Response

connection = pymysql.connect(host='localhost',
                             user='root',
                             db='comic',
                             use_unicode=True,
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)

KEY_PASSWORD = 'Key Password'


@app.route('/getComicOffset')
def getComicOffset():
    try:
        token = request.headers.get('token')
        offset = request.args.get('offset')
        count = request.args.get('count')
        if not token:
            return Response(json.dumps({'success': False, 'message': 'Invalid Token'}), mimetype='application/json')
        mycursor = connection.cursor()
        if validToken(mycursor, token):
            mycursor.execute("SELECT * FROM comic LIMIT %s,%s" % (offset, count))
            comics = mycursor.fetchall()
            for comic in comics:
                mycursor.execute("SELECT * FROM genre WHERE idcomic = %s" % comic['id'])
                comic['genre'] = mycursor.fetchall()
            mycursor.close()
            return Response(json.dumps({'success': True, 'result': comics}), mimetype='application/json')
        else:
            mycursor.close()
            return Response(json.dumps({'success': False, 'message': 'Invalid Token'}), mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({'success': False, 'message': str(e)}), mimetype='application/json')


@app.route('/getComic')
def getComic():
    try:
        token = request.headers.get('token')
        after = request.args.get('after')
        limit = request.args.get('limit')
        if not token:
            return Response(json.dumps({'success': False, 'message': 'Invalid Token'}), mimetype='application/json')
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
            return Response(json.dumps({'success': True, 'result': comics}), mimetype='application/json')
        else:
            mycursor.close()
            return Response(json.dumps({'success': False, 'message': 'Invalid Token'}), mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({'success': False, 'message': str(e)}), mimetype='application/json')


@app.route('/getComicImage/<int:id>')
def getComicImage(id):
    try:
        token = request.headers.get('token')
        after = request.args.get('after')
        limit = request.args.get('limit')
        # idComic = request.json
        # print(requestBody['id'] + " - " + requestBody['offset'] + " - " + requestBody['count'])
        if not token:
            return Response(json.dumps({'success': False, 'message': 'Invalid Token'}), mimetype='application/json')
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
            return Response(json.dumps({'success': True, 'result': data}), mimetype='application/json')
        else:
            mycursor.close()
            return Response(json.dumps({'success': False, 'message': 'Invalid Token'}), mimetype='application/json')
    except Exception as e:

        return Response(json.dumps({'success': False, 'message': str(e)}), mimetype='application/json')


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
        if mycursor.rowcount > 0:
            mycursor.close()
            return Response(json.dumps({'success': True}), mimetype='application/json')
        mycursor.close()
        return Response(json.dumps({'success': False}), mimetype='application/json')
    except HTTPError as e:
        response = e.args[0].response
        error = response.json()['error']['message']
        return Response(json.dumps({'success': False, 'message': error}), mimetype='application/json')


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
            if id :
                utoken = token_hex(32)
                sql = "UPDATE user SET token = %s WHERE id = %s"
                val = (utoken, str(id))
                mycursor.execute(sql, val)
                connection.commit()
                mycursor.close()
                return Response(json.dumps({'success': True, 'token': utoken}), mimetype='application/json')
            else:
                mycursor.close()
                return Response(json.dumps({'success': False, 'message': 'User Not Found'}), mimetype='application/json')
        else:
            return Response(json.dumps({'success': False, 'message': 'Verify email'}), mimetype='application/json')
    except HTTPError as e:
        response = e.args[0].response
        error = response.json()['error']['message']
        return Response(json.dumps({'success': False, 'message': error}), mimetype='application/json')

def validToken(cursor, token):
    cursor.execute(
        "SELECT COUNT(*) FROM user WHERE token = %s",
        (token)
    )
    count = cursor.fetchone()
    return count['COUNT(*)'] == 1


if __name__ == '__main__':
    app.run(host="192.168.7.152", debug=True)
