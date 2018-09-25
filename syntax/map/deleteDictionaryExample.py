# (Key,Value) = (Tên, Số điện thoại)
contacts = {"John": "01217000111", "Tom": "01234000111", "Addison": "01217000222", "Jack": "01227000123"}

print("Contacts: ", contacts)

print("\n")
print("Delete key = 'John' ")

# Xóa một phần tử ứng với khóa 'John'
del contacts["John"]

print("Contacts (After delete): ", contacts)

print("\n")
print("Delete key = 'Tom' ")

# Xóa một phần tử ứng với khóa 'Tom'
contacts.__delitem__("Tom")

print("Contacts (After delete): ", contacts)

print("Clear all element")

# Xóa toàn bộ các phần tử.
contacts.clear()

print("Contacts (After clear): ", contacts)

# Xóa luôn dictionary 'contacts' khỏi bộ nhớ
del contacts

# Lỗi xẩy ra khi truy cập vào biến không tồn tại trên bộ nhớ
print("Contacts (After delete): ", contacts)