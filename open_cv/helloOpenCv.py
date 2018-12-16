import cv2

# flags = 0 : ảnh trắng đen , 1 : ảnh màu
img = cv2.imread('girl.png', 1)
# draw line on image exist
cv2.line(img, (0, 0), (300, 400), (255, 0, 0), 5)
cv2.imwrite('girl2.png', img)
img2 = cv2.imread('girl2.png', 1)
#  show ảnh ( Default sẽ tự tắt sau khi mở
cv2.imshow('image', img2)
#  đóng bằng tay
cv2.waitKey(0)
#  Giải phóng bộ nhớ
cv2.destroyAllWindows()