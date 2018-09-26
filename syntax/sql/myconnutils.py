import pymysql

# Hàm trả về một connection.
def getConnection():
    # Bạn có thể thay đổi các thông số kết nối.
    connection = pymysql.connect(host='localhost',
                                 user='namtran',
                                 password='123456',
                                 db='simplehr',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection