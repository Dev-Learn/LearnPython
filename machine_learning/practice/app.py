import numpy as np
import pandas as pd
import matplotlib.pyplot as mp
import sklearn.linear_model as lm
from sklearn.metrics import r2_score,mean_absolute_error,mean_squared_error
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline

"""
    Demo Supervised Learning - Regression dùng Linear Model
"""

# load data
df = pd.read_csv('svdata.csv')
# print(df)
# print(df.describe())
# just draw point on đồ thị
# df.plot.scatter(x='learninghours',y='grade')
# plot của matplotlib là dạng đồ thị line
# mp.plot(df['learninghours'],df['grade'])
# mp.show()

# y = ax + b

lr = lm.LinearRegression()
# Sử dụng numpy.newaxis để tăng số dimemsions của matrix, với câu lệnh trên ( column vector )
#  khi này [1,2] sẽ thành [[1],[2]]
x = df['learninghours'][:,np.newaxis]
y = df['grade']
# train model using training data
lr.fit(x,y)
# đầu ra dự đoán
df['gradepred'] = lr.predict(x)
# trong hàm số ở trên y = ax + b thì sau khi train sẽ lấy đc a,b (a => intercept || b => coef_)
print('intercept : %s \n coeffient: %s' %(lr.intercept_,lr.coef_))
intercept = lr.intercept_
coef = lr.coef_

mp.scatter(x,y,color='black')
mp.plot(x,df.gradepred,color='green')


# Sau khi giải bài toán vói dữ liệu test và có đc các giá trị a,b ta cần đánh giá model của mình tốt đến mức nào
# Có 3 thông số đánh giá một model :
# - R-square
#           ~ thông số phồ biến đánh giá mô hình đưa ra fit đến mức độ nào so với dữ liệu
#           ~ có giá trị từ 0 -> 1 . Cần gần 1 càng tốt
#           ~ công thức : sum(SSR)/sum(SST) trong đó :
#                          * SSR : sum of square residual => square residual = sqr(y predict - mean (y real))
#                          * SST : sum of square total => square total = sqr(y real - mean(y real))
# - RMSE
#           - Root Mean Square Error
#           - Mô tả độ chính xác của dữ liệu tính toán vs dữ liệu thật
# - MAE
#           - Mean Absolute Error
#           - Đo độ lỗi dựa trên giá trị tuyệt đối
# - Cả 3 thông số đều có trong thư viên sklearn(sklearn.metrics): R-Square(r2_score),MAE(mean_absolute_error),RMSE(mean_squared_error)

print('R2 : %s' % r2_score(y,df.gradepred))
print('MAE : %s' % mean_absolute_error(y,df.gradepred))
print('RMSE : %s' % np.square(mean_squared_error(y,df.gradepred)))

model = make_pipeline(PolynomialFeatures(4),lr)
model.fit(x,y)
df['gradeData'] = model.predict(x)
mp.plot(x,df.gradeData,color='red')
mp.show()

print('R2 : %s' % r2_score(y,df.gradeData))
print('MAE : %s' % mean_absolute_error(y,df.gradeData))
print('RMSE : %s' % np.square(mean_squared_error(y,df.gradeData)))