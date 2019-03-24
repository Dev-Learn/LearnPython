import pymysql
from flask import Flask, make_response,request
import time
import json

# Kết nối vào database.
connection = pymysql.connect(host='localhost',
                             user='root',
                             db='learnFlutter',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)


def insertTodosTable():
    try:
        mycursor = connection.cursor()
        duedate = time.strftime('%Y-%m-%d %H:%M:%S')
        sql = 'INSERT INTO `todos` (`name`,`priority`,`description`,`duedate`) VALUES (%s, %s, %s, %s)'
        val = [
            ('Python', 1, 'Learn every thing about Python', duedate),
            ('Flutter', 1, 'Learn every thing about Flutter', duedate),
            ('Android', 1, 'Learn every thing about Android', duedate),
        ]
        mycursor.executemany(sql, val)
        connection.commit()
    finally:
        connection.close()


def insertTaskFollowIdToDo():
    try:
        mycursor = connection.cursor()
        # mycursor.execute(
        #     'CREATE TABLE IF NOT EXISTS tasks (id INT AUTO_INCREMENT PRIMARY KEY, todoId INT, name VARCHAR(255), isFinish BOOLEAN)')
        mycursor.execute('SELECT * FROM `todos`')
        data = mycursor.fetchall()
        for item in data:
            sql = 'INSERT INTO `tasks` (`todoId`,`name`,`isFinish`) VALUES (%s, %s, %s)'
            # Python
            if item['id'] == 1:
                val = [
                    (item['id'], 'Syntax', True),
                    (item['id'], 'Scrape Data', True),
                    (item['id'], 'Flask', True),
                    (item['id'], 'Django', True),
                    (item['id'], 'Machien Learning', False),
                ]
            # Flutter
            elif item['id'] == 2:
                val = [
                    (item['id'], 'Syntax', True),
                    (item['id'], 'API', True),
                    (item['id'], 'Animation', False),
                ]
            # Android
            else:
                val = [
                    (item['id'], 'Animation', True),
                    (item['id'], 'API', True),
                    (item['id'], 'View', True),
                    (item['id'], 'Architecture Component', True),
                    (item['id'], 'Clean Architecture', True),
                    (item['id'], 'FireBase', True),
                    (item['id'], 'Google Map', True),
                ]
            mycursor.executemany(sql, val)
            connection.commit()
    finally:
        connection.close()


@app.route('/todos')
def getAllTodos():
    try:
        mycursor = connection.cursor()
        mycursor.execute('SELECT * FROM `todos`')
        data = {'success': True, 'results': mycursor.fetchall()}
        return make_response(json.dumps(data))
    except Exception as e:
        print("Error %s" % e)
    # finally:
    #     connection.close()\
    return make_response(json.dumps({'success' : False}))

@app.route('/task',methods=['POST'])
def getTaskFollowIdToDo():
    try:
        id = request.form.get('todoId')
        # try:
        mycursor = connection.cursor()
        mycursor.execute('SELECT * FROM `tasks` WHERE todoId = %s' % id)
        data = {'success': True, 'results': mycursor.fetchall()}
        return make_response(json.dumps(data))
    except Exception as e:
        print("Error %s" % e)
    return make_response(json.dumps({'success': False}))

@app.route('/update_task', methods= ['PUT'])
def updateTask():
    try:
        data = request.json
        print(data['id'])
        print(data['name'])
        print(data['todoId'])
        print(data['isFinish'])
        mycursor = connection.cursor()
        sql = "UPDATE `tasks` SET `name` = %s , `isFinish` = %s WHERE `id` = %s"
        val = (data['name'], data['isFinish'],data['id'])
        mycursor.execute(sql, val)
        connection.commit()
        if(mycursor.rowcount > 0):
            return make_response(json.dumps({'success': True}))
    except Exception as e:
        print("Error %s" % e)
    return make_response(json.dumps({'success': False}))

@app.route('/create_task', methods= ['POST'])
def createTask():
    try:
        data = request.json
        print(data['id'])
        print(data['name'])
        print(data['todoId'])
        print(data['isFinish'])
        mycursor = connection.cursor()
        sql = "INSERT INTO `tasks` (todoId, name, isFinish) VALUES (%s, %s, %s)"
        val = (data['todoId'], data['name'],data['isFinish'])
        mycursor.execute(sql, val)
        connection.commit()
        if(mycursor.rowcount > 0):
            return make_response(json.dumps({'success': True}))
    except Exception as e:
        print("Error %s" % e)
    return make_response(json.dumps({'success': False}))

@app.route('/delete_task', methods= ['DELETE'])
def deleteTask():
    try:
        id = request.args.get('id')
        mycursor = connection.cursor()
        sql = "DELETE FROM `tasks` WHERE `id` = %s"
        val = (id)
        mycursor.execute(sql, val)
        connection.commit()
        if(mycursor.rowcount > 0):
            return make_response(json.dumps({'success': True}))
    except Exception as e:
        print("Error %s" % e)
    return make_response(json.dumps({'success': False}))


if __name__ == '__main__':
    # insertTodosTable()
    # insertTaskFollowIdToDo()
    # app.run(host='192.168.7.61',debug=True)
    app.run(debug=True)
