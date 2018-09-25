class Person(object):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # Ghi đè phương thức __eq__
    def __eq__(self, other):
        return self.name == other.name and self.age == other.age


jack1 = Person('Jack', 23)
jack2 = Person('Jack', 23)

# Gọi tới phương thức __eq__
print("jack1 == jack2 ?", jack1 == jack2)  # True

print("jack1 is jack2 ?", jack1 is jack2)  # False