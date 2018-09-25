class A: pass


class B(A): pass


# True
print("isinstance('abc', object): ", isinstance('abc', object))

# True
print("isinstance(123, object): ", isinstance(123, object))

b = B()
a = A()

# True
print("isinstance(b, A): ", isinstance(b, A))
print("isinstance(b, B): ", isinstance(b, B))

# False
print("isinstance(a, B): ", isinstance(a, B))

# B is subclass of A? ==> True
print("issubclass(B, A): ", issubclass(B, A))

# A is subclass of B? ==> False
print("issubclass(A, B): ", issubclass(A, B))