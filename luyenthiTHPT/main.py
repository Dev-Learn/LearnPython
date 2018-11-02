import json
from secrets import token_hex

import os
import pymysql
from flask import Flask, make_response, request

connection = pymysql.connect(host='localhost',
                             user='root',
                             db='trannamm_LuyenThi',
                             use_unicode=True,
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

app = Flask(__name__)


def insertData(cursor, sql, val):
    cursor.execute(sql, val)
    connection.commit()
    return cursor.lastrowid


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        print(data['idfacebook'])
        print(data['imei'])
        print(data['phone'])
        print(data['name'])
        print(data['picture'])
        print(data['email'])
        print(data['gender'])
        cursor = connection.cursor()
        cursor.execute(
            "SELECT `id`,COUNT(*) FROM TAIKHOAN WHERE idfacebook = %s",
            (data['idfacebook'],)
        )
        # gets the number of rows affected by the command executed
        count = cursor.fetchone()
        utoken = token_hex(32)
        if count['COUNT(*)'] == 0:
            # register
            sql = "INSERT INTO `TAIKHOAN` (idfacebook, imei, token) VALUES (%s, %s, %s)"
            val = (data['idfacebook'], data['imei'], utoken)
            idUser = insertData(cursor, sql, val)
            if idUser:
                sql = "INSERT INTO `THONGTINTAIKHOAN` (idUser,name,picture,gender,email,phone) VALUES(%s,%s,%s,%s,%s,%s)"
                val = (idUser, data['name'], data['picture'], data['gender'], data['email'], data['phone'])
                if insertData(cursor, sql, val):
                    return make_response(json.dumps({'success': True, 'token': utoken}))
                else:
                    return make_response(json.dumps({'success': False, 'message': 'Error'}))
            else:
                return make_response(json.dumps({'success': False, 'message': 'Error'}))
        else:
            # Login success
            sql = "UPDATE `TAIKHOAN` SET `imei` = %s , `token` = %s WHERE `id` = %s"
            val = (data['imei'], utoken, count['id'])
            cursor.execute(sql, val)
            connection.commit()
            if (cursor.rowcount > 0):
                return make_response(json.dumps({'success': True, 'token': utoken}))
    except Exception as e:
        return make_response(json.dumps({'success': False, 'message': str(e)}))


def validToken(cursor, token):
    cursor.execute(
        "SELECT COUNT(*) FROM TAIKHOAN WHERE token = %s",
        (token)
    )
    count = cursor.fetchone()
    return count['COUNT(*)'] == 1


@app.route('/uploadInfo', methods=['POST'])
def updateInfo():
    try:
        token = request.headers.get('token')
        cursor = connection.cursor()
        if validToken(cursor, token):
            id = request.form.get('id')
            name = request.form.get('name')
            gender = request.form.get('gender')
            email = request.form.get('email')
            phone = request.form.get('phone')

            print('id : %s, name : %s, gender : %s, email : %s, phone : %s' % (id, name, gender, email, phone))

            target = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pictures')
            print(target)

            if not os.path.isdir(target):
                os.mkdir(target)

            sql = "UPDATE `THONGTINTAIKHOAN` SET `name` = %s , `gender` = %s, `email` = %s, `phone` = %s"
            val = [name, gender, email, phone]

            file = request.files['picture']
            if file:
                filename = file.filename
                destination = '/'.join([target, filename])
                print(destination)
                file.save(destination)
                sql += ", `picture` = %s"
                val.append(destination)

            sql += " WHERE `id` = %s"
            val.append(id)

            val = tuple(val)

            cursor.execute(sql, val)
            connection.commit()

            if cursor.rowcount > 0:
                return make_response(json.dumps({'success': True}))
        else:
            return make_response(json.dumps({'success': False, 'error': 'Invalid Token'}))
    except Exception as e:
        return make_response(json.dumps({'success': False, 'message': str(e)}))

@app.route('/getSubject')
def getSubject():
    try:
        token = request.headers.get('token')
        cursor = connection.cursor()
        if validToken(cursor, token):
            cursor.execute("SELECT * FROM Subject")
            result = cursor.fetchall()
            return make_response(json.dumps({'success': True, 'result': result}))
        else:
            return make_response(json.dumps({'success': False, 'error': 'Invalid Token'}))
    except Exception as e:
        return make_response(json.dumps({'success': False, 'message': str(e)}))

# def createSubject():
#     try:
#         mycursor = connection.cursor()
#         mycursor.execute(
#             'CREATE TABLE IF NOT EXISTS Subject (id INT PRIMARY KEY, name VARCHAR(255), image VARCHAR(255)) DEFAULT CHARSET=utf8')
#         data = [{'id': 1, 'name': 'Sinh Học',
#                  'image': 'http://onthitot.com/wp-content/uploads/2018/01/de-cuong-on-tap-sinh-hoc-chuong-1-lop-12.jpg'},
#                 {'id': 2, 'name': 'Vật Lý',
#                  'image': 'http://img.giaoduc.net.vn/w801/Uploaded/2018/edxwpcqdh/2018_02_12/vatli_1.jpg'},
#                 {'id': 3, 'name': 'Hóa Học',
#                  'image': 'http://file.kenhsinhvien.vn/2015/07/21/chemistry-icons-and-formulas-on-the-school-board.jpg'},
#                 {'id': 4, 'name': 'Địa Lý',
#                  'image': 'https://s3-ap-southeast-1.amazonaws.com/img.spiderum.com/sp-images/12d715c0b12911e69277c7d42f3bb41c.png'},
#                 {'id': 5, 'name': 'Anh Văn',
#                  'image': 'http://www.daykemvungtau.vn/wp-content/uploads/2016/11/giao-vien-day-kem-anh-van-tai-nha-vung-tau.jpg'},
#                 {'id': 6, 'name': 'Toán',
#                  'image': 'https://3.bp.blogspot.com/-tqe7CkGVPjc/WhrRodntaDI/AAAAAAAADQE/MnrcvB9VHqEtEIvTzxflx_E9v0qNOnkiwCLcBGAs/s1600/maths.jpg'},
#                 {'id': 7, 'name': 'Lịch Sử',
#                  'image': 'https://kinhnghiemkhoinghiep.net/wp-content/uploads/2017/11/6-cach-hoc-mon-lich-su-lop-8-nhanh-thuoc-nho-lau-Copy.jpg'},
#                 {'id': 8, 'name': 'Ngữ Văn',
#                  'image': 'http://img.giaoduc.net.vn/w801/Uploaded/2018/edxwpcqdh/2018_01_22/vanhoc.jpg'}]
#         for item in data:
#             sql = 'INSERT INTO Subject (id, name,image) VALUES (%s, %s, %s)'
#             val = (item['id'], item['name'], item['image'])
#             mycursor.execute(sql, val)
#             connection.commit()
#     finally:
#         connection.close()


@app.route('/getTest', methods=['POST'])
def getTest():
    try:
        token = request.headers.get('token')
        cursor = connection.cursor()
        if validToken(cursor, token):
            data = request.json
            print(data['id'])
            print(data['number'])
            cursor.execute("SELECT * FROM CAUHOIVADAPAN WHERE idMON = %s LIMIT %s" % (data['id'],data['number']))
            result = cursor.fetchall()
            return make_response(json.dumps({'success': True, 'result': result}))
            pass
        else:
            return make_response(json.dumps({'success': False, 'error': 'Invalid Token'}))
    except Exception as e:
        return make_response(json.dumps({'success': False, 'message': str(e)}))

if __name__ == '__main__':
    app.run(debug=True)
    # createSubject()
