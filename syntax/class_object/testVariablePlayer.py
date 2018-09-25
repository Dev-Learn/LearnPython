from syntax.class_object.player import Player

player1 = Player("Tom", 20)

player2 = Player("Jerry", 20)

# Truy cập thông qua tên lớp.
print("Player.minAge = ", Player.minAge)

# Truy cập thông qua đối tượng.
print("player1.minAge = ", player1.minAge)
print("player2.minAge = ", player2.minAge)

print(" ------------ ")

print("Assign new value to minAge via class name, and print..")

# Gán một giá trị mới cho minAge thông qua tên lớp.
Player.minAge = 19

print("Player.minAge = ", Player.minAge)
print("player1.minAge = ", player1.minAge)
print("player2.minAge = ", player2.minAge)