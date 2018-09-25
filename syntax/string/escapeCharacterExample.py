# Hai ký tự TAB ngăn cách giữa "Hello World" và "Hello Python".
mystr = "Hello World\t\tHello Python"

print(mystr)

# Hai ký tự xuống dòng ngăn cách giữa "Hello World" và "Hello Python".
mystr = "Hello World\n\nHello Python"

print(mystr)

# Ký hiệu với dấu xoẹt	Mã trong hệ cơ số 16	    Mô tả
# \a	                    0x07	            Bell or alert
#
# \b	                    0x08	            Backspace
#
# \cx	 	                                    Control-x
#
# \C-x	 	                                    Control-x
#
# \e	                    0x1b	            Escape
#
# \f	                    0x0c	            Formfeed
#
# \M-\C-x	 	                                Meta-Control-x
#
# \n	                    0x0a	            Newline
#
# \nnn	                     	                Octal notation, where n is in the range 0.7
#
# \r	                    0x0d	            Carriage return
#
# \s	                    0x20	            Space
#
# \t	                    0x09	            Tab
#
# \v	                    0x0b	            Vertical tab
#
# \x	                     	                Character x
#
# \xnn	                     	                Hexadecimal notation, where n is in the range 0.9, a.f, or A.F


# Toán tử	                                                    Mô tả	                                                    Ví dụ
# +	                                    Nối (concatenate) 2 string, tạo thành một string mới.
#
#                                                                                                                       "Hello" +"Python" ==> "Hello Python"
# *	                                    Tạo một string mới bằng cách nối (concatenate) nhiều lần bản copy               "Hello"*2 ==> "HelloHello"
#                                       của cùng môt string.
#
# []	                                Trả về ký tự tại vị trí cho bởi chỉ số.	                                            a = "Hello"
#                                                                                                                           a[1] ==> "e"
# [ : ]	                                Trả về một chuỗi con chứa các ký tự cho bởi phạm vi (range)	                        a = "Hello"
#                                                                                                                           a[1:4] ==> "ell"
#                                                                                                                           a[1: ] ==> "ello"
# in	                                Trả về True nếu ký tự tồn tại trong string đã cho.	                                a = "Hello"
#                                                                                                                           'H' in a ==> True
# not in	                            Trả về True nếu ký tự không tồn tại trong string đã cho.	                        a = "Hello"
#                                                                                                                           'M' not in a ==> True
# r/R	                                Chuỗi thô (Raw String) - Ngăn chặn ý nghĩa thực tế của các ký tự thoát
#                                       (Escape character). Cú pháp cho chuỗi thô giống hệt với chuỗi thông thường          print (r'\n\t') ==> \n\t
#                                       ngoại trừ "toán tử chuỗi thô", chữ "r" đứng trước dấu ngoặc kép. "R" có thể         print (R'\n\t') ==> \n\t
#                                       là chữ thường (r) hoặc chữ hoa (R) và phải được đặt ngay trước dấu trích dẫn
#                                       đầu tiên.
#
# %	                                    Định dạng string	                                                                Xem tại phần dưới.