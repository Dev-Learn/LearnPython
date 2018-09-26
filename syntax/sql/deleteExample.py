# Sử dụng module tiện ích của bạn.
from syntax.sql import myconnutils

connection = myconnutils.getConnection()

print("Connect successful!")

try:
    cursor = connection.cursor()

    sql = "Delete from Salary_Grade where Grade = %s"

    # Thực thi sql và truyền 1 tham số
    rowCount = cursor.execute(sql, (3))

    connection.commit()

    print("Deleted! ", rowCount, " rows")

finally:
    # Đóng kết nối
    connection.close()