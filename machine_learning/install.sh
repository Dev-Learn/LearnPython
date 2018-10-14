#!/usr/bin/env bash
pip install numpy scipy matplotlib ipython jupyter pandas sympy nose keras sklearn

# ipython
# - Enhanced interactive console

# numpy
# - core lib for scientific computing
# - Là 1 thư viện core cung cấp các đối tượng mảng nhiều chiều công suất cao và các công cụ làm việc với các mảng này
# - ebook : Guide to Numpy - Travis Oliphant

# Scipy
# - Thư viện cơ bản cho việc tính toán của môn KHMT

# Matplolib
# - Thư viện hổ trợ đồ họa trong python
# - Thường được dùng để vẻ đồ thị , biểu diễn dữ liệu và phân bố một cách trực quan

# Pandas
# - Thư viện Python cung cấp các đối tượng ( cấu trúc ) và công cụ hổ trợ để làm việc , phân tích với dữ liệu dán nhãn hay relational
# data giống như SQL trong relation db
# - Phù hợp vs kiểu dữ liệu hàng cột như excel hay mysql,...
# - Sử dụng 2 kiểu dữ liệu mới là Serius và DataFrame đều xây dựng trên nên Numpy

# Scipy.org
# - Scientific Python là 1 hệ sinh thái bao gồm các thư viện cơ bản phục vụ cho scientific & math
# - Trong đó có : Numpy , Scipy, Matplolib, iPython, Sympy, Pandas ...

# sklearn
# - Rất nhiều hàm đc phát triển từ Scipy
# - Cung cấp 1 lượng thư viện đầy đủ cho các thuật toán của ML

# statsmodels
# - Mốt gói bổ sung cho sklearn với các phần thống kê kết quả cho các mô hình
# - Dữ liệu được chia ra làm 2 phần chính là : object và attribute
# - Về cơ bản có 2 loại biến : rời rạc ( Discrete or qualitative ) và liên tục ( Continuous or quatitative )
# - Scales of measurement : có 4 mức -> Nominal Scales of Measurement
#                                  -> Ordinal Scales of Measurement
#                                  -> Interval Scales of Measurement
#                                  -> Ratio Scales of Measurement