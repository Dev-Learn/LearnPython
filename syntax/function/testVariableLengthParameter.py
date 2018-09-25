# Truyền vào: *others = []
from syntax.function.variableLengthParameterExample import sumValues

a = sumValues(10, 20)

print("sumValues(10, 20) = ", a)

# Truyền vào: *others = [1]
a = sumValues(10, 20, 1)

print("sumValues(10, 20, 1 ) = ", a)

# Truyền vào: *others = [1,2]
a = sumValues(10, 20, 1, 2)

print("sumValues(10, 20, 1 , 2) = ", a)

# Truyền vào: *others = [1,2,3,4,5]
a = sumValues(10, 20, 1, 2, 3, 4, 5)

print("sumValues(10, 20, 1, 2, 3, 4, 5) = ", a)