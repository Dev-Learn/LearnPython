import cv2
import numpy as np

img = cv2.imread('girl2.png', 1)
# cv2.imshow('image', img)
# cv2.waitKey()
# cv2.destroyAllWindows()

# px = img[0, 0]
# print(px)

# [r,g,b]

# for i in range(100):
#     img[i, i] = [150, 50, 50]
#     img[i + 3, i + 3] = [1, 1, 1]
#
# cv2.imwrite('girl3.png', img)
# img2 = cv2.imread('girl3.png', 1)
# cv2.imshow('image', img2)
# cv2.waitKey()
# cv2.destroyAllWindows()

for i in range(200):
    for j in range(200):
        if img[i, j, 0] > 30:
            img[i, j] = 1

cv2.imwrite('girl5.png', img)
img2 = cv2.imread('girl5.png', 1)
cv2.imshow('image', img2)
cv2.waitKey()
cv2.destroyAllWindows()
