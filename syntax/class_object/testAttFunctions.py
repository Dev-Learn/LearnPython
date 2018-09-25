from syntax.class_object.player import Player

player1 = Player("Tom", 20)

# getattr(obj, name[, default])
print("getattr(player1,'name') = ", getattr(player1, "name"))

print("setattr(player1,'age', 21): ")

# setattr(obj,name,value)
setattr(player1, "age", 21)

print("player1.age = ", player1.age)

# Kiểm tra player1 có thuộc tính (attribute) address hay không?
hasAddress = hasattr(player1, "address")

print("hasattr(player1, 'address') ? ", hasAddress)

# Tạo thuộc tính 'address' cho đối tượng 'player1'.
print("Create attribute 'address' for object 'player1'")
setattr(player1, 'address', "USA")

print("player1.address = ", player1.address)

# Xóa thuộc tính 'address'.
delattr(player1, "address")