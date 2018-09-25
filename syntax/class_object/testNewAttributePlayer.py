from syntax.class_object.player import Player

player1 = Player("Tom", 20)

player2 = Player("Jerry", 20)

# Tạo một thuộc tính có tên 'address' cho player1.
player1.address = "USA"

print("player1.name = ", player1.name)
print("player1.age = ", player1.age)
print("player1.address = ", player1.address)

print(" ------------------- ")

print("player2.name = ", player2.name)
print("player2.age = ", player2.age)

# player2 không có thuộc tính 'address' (Lỗi xẩy ra tại đây).
# print("player2.address = ", player2.address)