# In ra danh sách các thuộc tính (attribute), phương thức và biến của lớp Player.
from syntax.class_object.player import Player

print(dir(Player))

print("\n\n")

player1 = Player("Tom", 20)

player1.address = "USA"

# In ra danh sách các thuộc tính, phương thức và biến của đối tượng 'player1'.
print(dir(player1))