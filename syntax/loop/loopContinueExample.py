print("Continue example")

# Khai báo một biến và gán giá trị 2
x = 2

while (x < 7):
    print("----------------------\n")
    print("x = ", x)

    # % : Là phép chia lấy số dư.
    # Nếu x là số chẵn, thì bỏ qua các lệnh bên dưới của 'continue'
    # để tiếp tục bước lặp (iteration) mới.
    if (x % 2 == 0):
        # Increase x by 1.
        x = x + 1
        continue

    else:
        # Increase x by 1.
        x = x + 1

        print("x after + 1 =", x)

print("End of example")