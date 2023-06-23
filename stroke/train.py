import pandas as pd
import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout
from sklearn.model_selection import train_test_split
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import KNNImputer
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split

#Load data
df = pd.read_csv('resources/stroke.csv', index_col='id')

#removes labels from dataset
X, y = df.drop('stroke', axis=1).values, df['stroke'].values

#Encodes catagoric variables
cat_ix = [0, 4, 5, 6, 9] #index of catagoric variables
cat_ct = ColumnTransformer([
    ('cat_vars', OneHotEncoder(), cat_ix)
], remainder='passthrough')
X_encoded = cat_ct.fit_transform(X)

#Impute missing values
#create Kmodel imputer object
knn_imp = KNNImputer(n_neighbors=5)
X_imputed = knn_imp.fit_transform(X_encoded)

#Scale Numeric Variables
num_ix = [16, 19, 20] #index of numeric variables
num_ct = ColumnTransformer([
    ('num_vars', StandardScaler(), num_ix)
], remainder='passthrough')
X_scaled = num_ct.fit_transform(X_imputed)

#Splits the data into train, test, validate
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=8)
X_val, X_test, y_val, y_test = train_test_split(X_test, y_test, test_size=0.5, random_state=8)

#SMOTE for class balancing
sm = SMOTE(random_state=8)

#create new training set with SMOTE object
X_bal, y_bal = sm.fit_resample(X_train, y_train)

n_features = X_train.shape[1]

#builds the architecture for a neural network
model = Sequential()
model.add(Dense(32, activation='relu', kernel_initializer='he_normal', input_shape=(n_features,)))
model.add(Dense(16, activation='relu', kernel_initializer='he_normal'))
model.add(Dense(2, activation='relu', kernel_initializer='he_normal'))
model.add(Dropout(0.6))
model.add(Dense(1, activation='sigmoid'))

#Compile the model with Adam optimizer
model.compile(optimizer="adam", loss='binary_crossentropy', metrics=['accuracy'])

#Trains the neural network
model.fit(X_bal, y_bal, epochs=200, batch_size=16, verbose=0)

#Save the model
joblib.dump(model, "model.joblib")