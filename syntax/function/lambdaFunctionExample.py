# Khai báo một biến: hello = một hàm nặc danh và không có tham số.
hello = lambda: "Hello"

# Khai báo một biến: mySum = một hàm nặc danh có 2 tham số.
mySum = lambda a, b: a + b

a = hello()

print(a)

a = mySum(10, 20)

print(a)