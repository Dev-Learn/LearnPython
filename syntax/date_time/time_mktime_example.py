import time

a_struct_time = time.localtime()

print("Current time as struct_time: ")
print(a_struct_time)

# Chuyển đổi struct_time hoặc Tuple thành Ticks.
ticks = time.mktime(a_struct_time)

print("Ticks: ", ticks)

# Một Tuple có 9 phần tử.
aTupleTime = (2017, 4, 15, 13, 5, 34, 0, 0, 0)

print("\n")
print("A Tuple represents time: ")
print(aTupleTime)

# Chuyển đổi struct_time hoặc Tuple thành Ticks.
ticks = time.mktime(aTupleTime)

print("Ticks: ", ticks)