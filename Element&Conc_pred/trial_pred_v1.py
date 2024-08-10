import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
import cv2


def pred_conc(data, img):
    log_conc = abs(np.log(data["Concentration"]))

    X = np.column_stack((data["Blue channel max. intensity"],data["Green channel max. intensity"], data["Red channel max. intensity"]))
    y = log_conc

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    model = DecisionTreeRegressor(max_depth=5)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    #print("Mean Squared Error:", np.exp(-mse))

    b, g, r = cv2.split(img)


    max_b = cv2.minMaxLoc(b)[1]
    max_g = cv2.minMaxLoc(g)[1]
    max_r = cv2.minMaxLoc(r)[1]

    sample_input = np.array([max_b,max_g,max_r]).reshape(1, -1) 
    sample_prediction = model.predict(sample_input)

    return np.exp(-sample_prediction[0])

data_Hg = pd.read_csv("Element&Conc_pred\Image_data_Hg.csv")
data_Cr = pd.read_csv("Element&Conc_pred\Image_data_Cr.csv")
data_Co = pd.read_csv("Element&Conc_pred\Image_data_Co.csv")

img = cv2.imread('Element&Conc_pred\chitkul plane water.jpg')

print(f"Chromium Concentration: {pred_conc(data_Cr,img)} M")
print(f"Mercury Concentration: {pred_conc(data_Hg,img)} M")
print(f"Cobalt Concentration: {pred_conc(data_Co,img)} M")