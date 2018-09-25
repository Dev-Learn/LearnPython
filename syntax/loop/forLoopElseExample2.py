print("For loop example")

# for x = 3, 4, 5, 6
for x in range(3, 7):

    print("Value of x = ", x)
    if x == 5:
        print("Break!")
        break

else:
    # Nếu lệnh break đã được gọi trong vòng lặp,
    # lệnh này sẽ không được thực thi.
    print("This command will not be executed!")

# Dòng lệnh này nằm ngoài khối lệnh for.
print("End of example")