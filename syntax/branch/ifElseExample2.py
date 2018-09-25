print("Please enter your age: \n")

# Khai báo một biến inputStr, lưu trữ dòng text người dùng nhập vào từ bàn phím.
inputStr = input()

# Hàm int(..) chuyển một chuổi thành 1 số tự nhiên
age = int(inputStr)

# In ra tuổi của bạn
print("Your age: ", age)

# Kiểm tra nếu age nhỏ hơn 80 thì ...
if (age < 80):

    print("You are pretty young")


# Ngược lại nếu tuổi nằm trong khoảng 80, 100 thì
elif (age >= 80 and age <= 100):

    print("You are old")

# Ngược lại (Các trường hợp còn lại)
else:
    print("You are very old")