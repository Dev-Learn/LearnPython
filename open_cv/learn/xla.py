import cv2
import numpy as np

img = cv2.imread('girl.png', 1)
# img = cv2.imread('girl.png', 0)
print(img.shape)
# (960, 768, 3) ==> 960 : chiều cao , 768 : chiều rộng , 3 : dạng ảnh có 3 kênh màu (r,n,g) ( ảnh màu )
# (960, 768) ==> 960 : chiều cao , 768 : chiều rộng ( ảnh trắng đen )
print(img.size)
# 2211840 : kích thước tấm hình ( byte )
print(img.dtype)
# uint8 : kiểu ảnh 8 bit

# Cắt hình ( dựa theo toa độ điểm )
#                 điểm ------------------------------------
#                   |                                     |
#                   |                                     |
#                   |                                     |
#                   |----------------------------------- điểm
#
# subimg = img[0:960, 0:768]
# subimg = subimg[:, :, 0]
# cv2.imshow('image', subimg)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

img2 = cv2.imread('scenery.jpg', 1)

subimg1 = img[0:400, 0:400]
subimg2 = img2[0:400, 0:400]

img3 = cv2.add(subimg1, subimg2)
cv2.imshow('image', img3)

cv2.waitKey(0)
cv2.destroyAllWindows()
