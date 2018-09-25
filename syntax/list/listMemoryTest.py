list1 = [1990, 1991, 1992]

print("list1: ", list1)

# Địa chỉ của list1 trên bộ nhớ.
list1Address = hex(id(list1))

print("Address of list1: ", list1Address)

print("\n")
print("Append element 2001 to list1")

# Nối (append) một phần tử vào list1.
list1.append(2001)

print("list1 (After append): ", list1)

# Địa chỉ của list1 trên bộ nhớ.
list1Address = hex(id(list1))

print("Address of list1 (After append): ", list1Address)