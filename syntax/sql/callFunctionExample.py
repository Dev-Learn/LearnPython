from syntax.sql import myconnutils

connection = myconnutils.getConnection()

print("Connect successful!")

try:
    cursor = connection.cursor()

    # Get_Employee_Info_Wrap
    # @p_Emp_Id       Integer
    v_Emp_No = ""

    inOutParams = (100)

    sql = "Select Get_Emp_No(%s) as Emp_No "

    cursor.execute(sql, (100))

    print(' ----------------------------------- ')

    for row in cursor:
        print('Row: ', row)
        print('Row[Emp_No]: ', row['Emp_No'])


finally:
    # Đóng kết nối (Close connection).
    connection.close()