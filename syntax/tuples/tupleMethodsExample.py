years = (1990, 1991, 1993, 1991, 1993, 1993, 1993)

print("Years: ", years)

print("\n")

# Trả về số lần xuất hiện của 1993
print("years.count(1993): ", years.count(1993))

# Tìm vị trí xuất hiện 1993
print("years.index(1993): ", years.index(1993))

# Tìm vị trí xuất hiện 1993, bắt đầu từ chỉ số 3
print("years.index(1993, 3): ", years.index(1993, 3))

# Tìm vị trí xuất hiện 1993, bắt đầu từ chỉ số 4 tới 5 (Không bao gồm 6)
print("years.index(1993, 4, 6): ", years.index(1993, 4, 6))