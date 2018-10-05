import pymysql as pymysql
import pymysql.cursors

# Kết nối vào database.
connection = pymysql.connect(host='localhost',
                             user='root',
                             db='simplehr',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

print("connect successful!!")

try:

    with connection.cursor() as cursor:

        # SQL
        sql = "SELECT Dept_No, Dept_Name FROM Department "

        # Thực thi câu lệnh truy vấn (Execute Query).
        cursor.execute(sql)

        print("cursor.description: ", cursor.description)

        print()

        for row in cursor:
            print(row)

finally:
    # Đóng kết nối (Close connection).
    connection.close()