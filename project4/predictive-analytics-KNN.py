# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 13:52:59 2024

@author: cassi
"""

import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import GridSearchCV
from math import sqrt

# figuring out plots
import matplotlib.pyplot as plt
import numpy as np
plt.figure(1)
plt.plot(range(10))
plt.figure(2)
plt.plot(np.random.rand(50))

file_path = 'C:/Users/cassi/OneDrive/Documents/School/CTU/Big_data_analytics/.spyder-py3/gait.csv'

df = pd.read_csv(file_path)

print(df.head())
print(df.columns.tolist())

''' problem statement: Predict if the person walking is wearing a knee brace, ankle brace, or no brace 
(condition = 2, 3 or 1) based on joint angle while they walk. 
'''

df.drop('subject', axis=1, inplace=True)

fig = px.histogram(df, x='condition') 
#plot(fig, auto_open=True)
fig.show(auto_open=True)

plt.figure(3)
df["condition"].hist(bins=3)
plt.show()

correlation_matrix = df.corr()
print(correlation_matrix['condition'])
'''' There is very low correlation between the person's condition and the way they walk. Therefore, the predictive ability
 of this program will not be very good. '''
 
# separate out the independent variables (X) and target variable (y)
X = df.drop('condition', axis=1)
y = df['condition']
 
# split data into training data and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=333)

# create a k nearest neighbor model that considers the 3 closest neighbors
knn_model = KNeighborsRegressor(n_neighbors=3)

# train the model/fit the model on the training data
knn_model.fit(X_train, y_train)

# see how accurate the predictive model is (on the training data) with root mean square error
train_predicts = knn_model.predict(X_train)
mse = mean_squared_error(y_train, train_predicts)
rmse = sqrt(mse)
print(rmse)

# see how accurate the predictive model is on the testing data
test_predicts = knn_model.predict(X_test)
mse = mean_squared_error(y_test, test_predicts)
rmse = sqrt(mse)
print(rmse)

