import numpy as np
import pandas as pandas
import matplotlib.pyplot as mpl

# Numpy
# # Mảng
# e = np.full((3,3),8)
# print(e)
# # Check size and type
# print(e.shape,e.dtype)
#
# e = np.random.random((3,3))
# print(e)
#
# e = np.eye(3)
# print(e)
#
# e = np.arange(10)
# print(e)
#
# e = np.arange(10,dtype=float)
# print(e)
#
# # Slice
# h =[1,2,3,4,5,6,7,8,9]
# # 1 : start index , 15 stop index, 2 step 0
# a = h[1:15:2]
# print(a)
# # step < 0 => negative way
# a = h[1:-5:-1]
# print(a)
# # 2 dimension array
# a = h[1:3:]
# print(a)

# Pandas
# s = pandas.Series([1,2,3,4,5],index=['r1','r2','r3','r4','r5'])
# print('Serius %s' % s)
# d = pandas.DataFrame({'col1' : ['v01','v02','v03'],
#                       'col2' : ['v11','v12','v13']
#                       }, columns=['col1','col2'])
# print('DataFrame %s' % d)

# Matplolib
x = np.arange(5)
y = (4,8,6,2,5)
mpl.bar(x,y)
mpl.show()