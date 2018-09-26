# Sử dụng module tiện ích của bạn.
import datetime

from syntax.sql import myconnutils

connection = myconnutils.getConnection()

print("Connect successful!")

try:
    cursor = connection.cursor()

    sql = "Update Employee set Salary = %s, Hire_Date = %s where Emp_Id = %s "

    # Hire_Date
    newHireDate = datetime.date(2002, 10, 11)

    # Thực thi sql và truyền 3 tham số.
    rowCount = cursor.execute(sql, (850, newHireDate, 7369))

    connection.commit()

    print("Updated! ", rowCount, " rows")

finally:
    # Đóng kết nối
    connection.close()