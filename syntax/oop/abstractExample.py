# Một lớp trừu tượng (Abstract class).
class AbstractDocument:
    def __init__(self, name):
        self.name = name

    # Một phương thức không thể sử dụng được, vì nó luôn ném ra lỗi.
    def show(self):
        raise NotImplementedError("Subclass must implement abstract method")


class PDF(AbstractDocument):
    # Ghi đè phương thức của lớp cha
    def show(self):
        print("Show PDF document:", self.name)


class Word(AbstractDocument):
    def show(self):
        print("Show Word document:", self.name)


# ----------------------------------------------------------
documents = [PDF("Python tutorial"),
             Word("Java IO Tutorial"),
             PDF("Python Date & Time Tutorial")]

for doc in documents:
    doc.show()