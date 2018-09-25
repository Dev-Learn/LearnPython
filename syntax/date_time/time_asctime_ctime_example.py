import time

# Một Tuple với 9 phần tử.
# (Year, month, day, hour, minute, second, wday, yday, isdst)
a_tuple_time = (2017, 4, 15, 22, 1, 29, 0, 0, 0)

a_timeAsString = time.asctime(a_tuple_time)

print("time.asctime(a_tuple_time): ", a_timeAsString)

a_struct_time = time.localtime()
print("a_struct_time: ", a_struct_time)

a_timeAsString = time.asctime(a_struct_time)

print("time.asctime(a_struct_time): ", a_timeAsString)

# Số giây tính từ 12h sáng ngày 1-1-1970 tới hiện tại.
ticks = time.time()

a_timeAsString = time.ctime(ticks)

print("time.ctime(ticks): ", a_timeAsString)