print("Break example")

# Tạo một biến x và gán giá trị 2 cho nó.
x = 2

while (x < 15):
    print("----------------------\n")
    print("x = ", x)

    # Kiểm tra nếu x = 5 thì thoát ra khỏi vòng lặp.
    if (x == 5):
        break

    # Tăng giá trị của x thêm 1
    x += 1
    print("x after + 1 = ", x)

print("End of example")