tuple1 = (1990, 1991, 1992)

print("tuple1: ", tuple1)

print("Concat (2001, 2002) to tuple1")

tuple2 = tuple1 + (2001, 2002)

print("tuple2: ", tuple2)

# Một Tuple con, chứa các phần tử từ chỉ số 1 đến 4 (1,2,3)
tuple3 = tuple2[1:4]

print("tuple2[1:4]: ", tuple3)

# Một Tuple con, chứa các phần tử từ chỉ số 1 đến cuối.
tuple4 = tuple2[1:]

print("tuple2[1: ]: ", tuple4)