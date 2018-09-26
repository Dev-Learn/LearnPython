from syntax.sql import myconnutils
# Sử dụng module tiện ích của bạn.

connection = myconnutils.getConnection()

print("Connect successful!")

sql = "Select Emp_No, Emp_Name, Hire_Date from Employee Where Dept_Id = %s "

try:
    cursor = connection.cursor()

    # Thực thi sql và truyền 1 tham số.
    cursor.execute(sql, (10))

    print("cursor.description: ", cursor.description)

    print()

    for row in cursor:
        print(" ----------- ")
        print("Row: ", row)
        print("Emp_No: ", row["Emp_No"])
        print("Emp_Name: ", row["Emp_Name"])
        print("Hire_Date: ", row["Hire_Date"], type(row["Hire_Date"]))

finally:
    # Đóng kết nối
    connection.close()