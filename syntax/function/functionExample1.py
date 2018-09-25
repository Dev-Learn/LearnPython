# Định nghĩa một hàm:
def sayHello(name):
    # Kiểm tra nếu name là rỗng (empty) hoặc null.
    if not name:
        print("Hello every body!")

    # Nếu name không rỗng và không null.
    else:
        print("Hello " + name)


# Gọi hàm, truyền tham số vào hàm.
sayHello("")

sayHello("Python")

sayHello("Java")