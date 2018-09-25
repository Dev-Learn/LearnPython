import time

# Một string đại diện thời gian.
aStringTime = "22-12-2007 23:30:59"

a_struct_time = time.strptime(aStringTime, "%d-%m-%Y %H:%M:%S")

print("a_struct_time:")

print(a_struct_time)