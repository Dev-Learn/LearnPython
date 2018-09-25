tuple1 = (1990, 1991, 1992)

# Địa chỉ của tuple1 trên bộ nhớ.
tuple1Address = hex(id(tuple1))

print("Address of tuple1: ", tuple1Address)

# Nối một tuple vào tuple1.
tuple1 = tuple1 + (2001, 2002)

# Địa chỉ của tuple1 trên bộ nhớ.
tuple1Address = hex(id(tuple1))

print("Address of tuple1 (After concat): ", tuple1Address)
