from flask import Flask, request, make_response
from secrets import token_hex
import json
import redis

app = Flask(__name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0)


# users = [{
#     'id' : '1',
#     'username' : 'namtran',
#     'password' : '123456',
#     'actived' : True
# },{
#     'id' : '2',
#     'username' : 'trannam',
#     'password' : '123456',
#     'actived' : True
# },{
#     'id' : '3',
#     'username' : 'trannamdev',
#     'password' : '123456',
#     'actived' : True
# }]


def getUsersFromRedis():
    getUsers = r.get('users')
    return json.loads(getUsers)


def checkLogin(username, password):
    """ Check user login and return result """
    users = getUsersFromRedis()
    user = [user for user in users if user['username'] == username and user['password'] == password]
    return user

def getUserFolowName(username):
    """ Get user follow username """
    users = getUsersFromRedis()
    for user in users:
        if user['username'] == username:
            return user


def saveUserToken(username, utoken, expire=60 * 30):
    """ Save the user token to the cache """
    r.setex('%s_token' % username, expire, utoken)
    return True

def checkUserToken(username,utoken):
    token = r.get('%s_token' %username)
    print('token : ' + str(token) + '\n' + 'utoken : ' + utoken)
    return token == utoken.encode('UTF-8')


@app.route('/test/api/login', methods=['POST'])
def doLogin():
    username = request.form.get('username')
    password = request.form.get('password')
    if checkLogin(username, password):
        utoken = token_hex(16)
        saveUserToken(username, utoken)
        result = {'result': True, 'token': utoken}
        return make_response(json.dumps(result))
    else:
        result = {'result': False}
        return make_response(json.dumps(obj=result))

@app.route('/test/api/users', methods=['GET'])
def getUsers():
    user = request.args.get('username')
    token = request.args.get('token')
    print('User : ' + user + '\n' + 'token : ' + token)
    if checkUserToken(user,token):
        result = {'result' : True, 'users' : getUsersFromRedis()}
        return make_response(json.dumps(result))
    else:
        result = {'result' : False, 'message' : 'Invalid Token'}
        return make_response(json.dumps(result))

@app.route('/test/api/user',methods=['POST'])
def getUser():
    user = request.form.get('username')
    token = request.args.get('token')
    print('User : ' + user + '\n' + 'token : ' + token)
    if checkUserToken(user, token):
        result = {'result': True, 'users': getUserFolowName(user)}
        return make_response(json.dumps(result))
    else:
        result = {'result': False, 'message': 'Invalid Token'}
        return make_response(json.dumps(result))

if __name__ == '__main__':
    # r.set('users', json.dumps(users))

    app.run(debug=True)
