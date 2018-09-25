print("Three")

value = 10 / 2

print("Two")

value = 10 / 1

print("One")

d = 0

try:
    # Phép chia này có vấn đề, chia cho 0.
    # Một lỗi được phát ra tại đây (ZeroDivisionError).
    value = 10 / d

    print("value = ", value)

except ZeroDivisionError as e:

    print("Error: ", str(e))
    print("Ignore to continue ...")

print("Let's go!")