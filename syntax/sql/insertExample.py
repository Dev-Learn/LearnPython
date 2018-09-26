# Sử dụng module tiện ích của bạn.
from syntax.sql import myconnutils

connection = myconnutils.getConnection()

print("Connect successful!")

try:
    cursor = connection.cursor()

    sql = "Select max(Grade) as Max_Grade from Salary_Grade "
    cursor.execute(sql)

    # 1 dòng dữ liệu
    oneRow = cursor.fetchone()

    # Output: {'Max_Grade': 4} or {'Max_Grade': None}
    print("Row Result: ", oneRow)

    grade = 1

    if oneRow != None and oneRow["Max_Grade"] != None:
        grade = oneRow["Max_Grade"] + 1

    cursor = connection.cursor()

    sql = "Insert into Salary_Grade (Grade, High_Salary, Low_Salary) " \
          + " values (%s, %s, %s) "

    print("Insert Grade: ", grade)

    # Thực thi sql và truyền 3 tham số
    cursor.execute(sql, (grade, 2000, 1000))

    connection.commit()

finally:
    connection.close()