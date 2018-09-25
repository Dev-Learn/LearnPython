years = [1990, 1991, 1992, 1993, 1993, 1993, 1994]

print("Years: ", years)

print("\n - Reverse the list")

# Đảo ngược danh sách.
years.reverse()

print("Years (After reverse): ", years)

aTuple = (2001, 2002, 2003)

print("\n - Extend: ", aTuple)
years.extend(aTuple)

print("Years (After extends): ", years)

print("\n - Append 3000")
years.append(3000)

print("Years (After appends): ", years)

print("\n - Remove 1993")
years.remove(1993)

print("Years (After remove): ", years)

print("\n - years.pop()")

# Loại bỏ phần tử cuối cùng của danh sách.
lastElement = years.pop()

print("last element: ", lastElement)

print("\n")

# Count
print("years.count(1993): ", years.count(1993))