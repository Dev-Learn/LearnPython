# Định nghĩa một hàm:
def getGreeting(name):
    # Kiểm tra nếu name là rỗng hoặc null (None).
    if not name:
        # Trả về một giá trị.
        # Và hàm sẽ kết thúc ở đây.
        return "Hello every body!"

    # Nếu name không rỗng và không null (Không None).
    # đoạn code dưới đây sẽ được thực thi.
    return "Hello " + name


# Gọi hàm, truyền tham số vào hàm.
greeting = getGreeting("")

print(greeting)

greeting = getGreeting("Python")

print(greeting)