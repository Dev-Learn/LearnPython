import time

# 1 giây sau kỷ nguyên máy tính (epoch).
# Hàm này trả về một kiểu struct: struct_time
ts = time.gmtime(1)

print("1 seconds after epoch: ")

print(ts)

print("\n")

# Thời điểm hiện tại, giống với time.gmtime( time.time() )
# Hàm này trả về một kiểu struct: struct_time
ts = time.gmtime()

print("struct_time for current time: ")
print(ts)