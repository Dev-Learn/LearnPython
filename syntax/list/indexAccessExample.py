fruitList = ["apple", "apricot", "banana", "coconut", "lemen", "plum", "pear"]

print(fruitList)

# Số phần tử.
print("Element count: ", len(fruitList))

for i in range(0, len(fruitList)):
    print("Element at ", i, "= ", fruitList[i])

# Một danh sách con chứa các phần tử từ index 1 đến 4 (1, 2, 3)
subList = fruitList[1: 4]

# ['apricot', 'banana', 'coconut']
print("Sub List [1:4] ", subList)