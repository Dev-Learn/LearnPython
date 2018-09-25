contacts = {"John": "01217000111", "Addison": "01217000222", "Jack": "01227000123"}

print("contacts: ", contacts)

print("Element count: ", len(contacts))

contactsAsString = str(contacts)

print("str(contacts): ", contactsAsString)

# Một đối tượng đại diện lớp 'dict'.
aType = type(contacts)

print("type(contacts): ", aType)

# Hàm dir(dict) trả về các thành viên của lớp 'dict'.
print("dir(dict): ", dir(dict))

# ------------------------------------------------------------------------------------
# ['__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__',
#  '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__',
#  '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__',
#  '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__',
#  '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', 'clear',
#  'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem',
#  'setdefault', 'update', 'values']
# -------------------------------------------------------------------------------------