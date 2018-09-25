# Python 3.x
class AgeException(Exception):
    def __init__(self, msg, age):
        super().__init__(msg)
        self.age = age


class TooYoungException(AgeException):
    def __init__(self, msg, age):
        super().__init__(msg, age)


class TooOldException(AgeException):
    def __init__(self, msg, age):
        super().__init__(msg, age)

        # Hàm kiểm tra tuổi, nó có thể ném ra ngoại lệ.


def checkAge(age):
    if (age < 18):
        # Nếu tuổi nhỏ hơn 18, một ngoại lệ sẽ bị ném ra.
        # Hàm sẽ bị kết thúc tại đây.
        raise TooYoungException("Age " + str(age) + " too young", age)

    elif (age > 40):
        # Nếu tuổi lớn hơn 40, một ngoại lệ sẽ bị ném ra
        # Hàm sẽ bị kết thúc tại đây.
        raise TooOldException("Age " + str(age) + " too old", age);

    # Nếu tuổi nằm trong khoảng 18-40.
    # Đoạn code này sẽ được thực thi.
    print("Age " + str(age) + " OK!");