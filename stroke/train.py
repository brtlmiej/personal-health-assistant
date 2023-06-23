import pandas as pd
import numpy as np
from tensorflow.keras import Input, Model
from tensorflow.keras.layers import Dense, Dropout
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import KNNImputer
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.wrappers.scikit_learn import KerasClassifier
from tensorflow import keras #keras
import tensorflow as tf #tensorflow
from sklearn.metrics import accuracy_score, recall_score ,precision_score, f1_score#evaluate model

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

#builds the architecture for a neural network
#creates a dense network with 1 skip step
inputs = Input(shape=(21,))
a = Dense(64, activation='relu')(inputs)
x = Dropout(0.6)(a)
x = Dense(128, activation='relu')(x)
x = Dropout(0.6)(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.6)(x)
x = Dense(128, activation='relu')(x)
x = Dropout(0.6)(x)
x = layers.concatenate([a, x])
x = Dense(64, activation='relu')(x)
x = Dropout(0.6)(x)
x = Dense(32, activation='relu')(x)
x = Dropout(0.6)(x)
output = Dense(1, activation='sigmoid')(x)

model = Model(inputs, output, name="stroke_predictor")

#Compile the model with Adam optimizer
model.compile(optimizer=tf.optimizers.Adam(learning_rate=0.0001),
            loss='binary_crossentropy', metrics=['accuracy'])
early_stopper = EarlyStopping(monitor='val_loss', patience=30, restore_best_weights=True)

#Trains the neural network
history = model.fit(X_bal, y_bal, epochs=1000, callbacks=[early_stopper], validation_data=(X_val, y_val), verbose=0)

#Save the model
joblib.dump(model, "model.joblib")