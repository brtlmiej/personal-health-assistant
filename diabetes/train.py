import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
import joblib

#Loading the dataset
df = pd.read_csv("resources/diabetes.csv")

#Defining x and y variable
x = df.drop(['Outcome'], axis=1).to_numpy()
y = df['Outcome'].to_numpy()

#ensure all data are floating point values
x = x.astype('float32')

#encode strings to integer
y = LabelEncoder().fit_transform(y)

#Creating Train and Test Datasets
x_train, x_test, y_train, y_test = train_test_split(x, y,test_size = 0.33)

# Determine the number of input features
n_features = x_train.shape[1]

#Defining the model
model = Sequential()
model.add(Dense(10, activation='relu', kernel_initializer='he_normal', input_shape=(n_features,)))
model.add(Dense(8, activation='relu', kernel_initializer='he_normal'))
model.add(Dense(1, activation='sigmoid'))

#Compiling the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

#Fitting the model
model.fit(x_train, y_train, epochs=200, batch_size=16, verbose=0)

#Prediction
#input_values = [[6, 148, 72, 35, 0, 33.6, 0.627, 50]]
#y_pred = model.predict(input_values)
#print('Predicted Output:', y_pred)

#Save model
joblib.dump(model, "model.joblib")