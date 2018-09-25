fruits = ("apple", "apricot", "banana", "coconut", "lemen", "plum", "pear")

print(fruits)

# Số phần tử.
print("Element count: ", len(fruits))

for i in range(0, len(fruits)):
    print("Element at ", i, "= ", fruits[i])

# Một Tuple con chứa các phần tử từ index 1 đến 4 (1, 2, 3)
subTuple = fruits[1: 4]

# ('apricot', 'banana', 'coconut')
print("Sub Tuple [1:4] ", subTuple)