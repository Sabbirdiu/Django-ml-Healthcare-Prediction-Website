from django.shortcuts import render
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
# Create your views here.
def index(request):
    return render(request,'index.html')


def diabetes(request):
    # Reading the training data set
    dfx = pd.read_csv('data/Diabetes_XTrain.csv')
    dfy = pd.read_csv('data/Diabetes_YTrain.csv')
    X = dfx.values
    Y = dfy.values
    Y = Y.reshape((-1,))

    # Reading data from user
    value = ''
    accuracy_rf = 0.0
    accuracy_knn = 0.0

    if request.method == 'POST':
        pregnancies = float(request.POST['pregnancies'])
        glucose = float(request.POST['glucose'])
        bloodpressure = float(request.POST['bloodpressure'])
        skinthickness = float(request.POST['skinthickness'])
        bmi = float(request.POST['bmi'])
        insulin = float(request.POST['insulin'])
        pedigree = float(request.POST['pedigree'])
        age = float(request.POST['age'])

        user_data = np.array(
            (pregnancies,
             glucose,
             bloodpressure,
             skinthickness,
             bmi,
             insulin,
             pedigree,
             age)
        ).reshape(1, 8)

        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        # Random Forest Classifier
        rf = RandomForestClassifier(n_estimators=100, criterion='gini', max_depth=5)
        rf.fit(X_train, y_train)
        y_pred_rf = rf.predict(X_test)
        accuracy_rf = accuracy_score(y_test, y_pred_rf)

        # K-Nearest Neighbors Classifier
        knn = KNeighborsClassifier(n_neighbors=3)
        knn.fit(X_train, y_train)
        y_pred_knn = knn.predict(X_test)
        accuracy_knn = accuracy_score(y_test, y_pred_knn)

        # Use the model with the highest accuracy for prediction
        if accuracy_rf >= accuracy_knn:
            predictions = rf.predict(user_data)
        else:
            predictions = knn.predict(user_data)

        if int(predictions[0]) == 1:
            value = 'Positive'
        elif int(predictions[0]) == 0:
            value = "Negative"

        print("Random Forest Accuracy:", accuracy_rf*100)
        print("K-Nearest Neighbors Accuracy:", accuracy_knn*100)

    return render(request,
                  'diabetes.html',
                  {
                      'context': value,
                      'accuracy_rf': accuracy_rf,
                      'accuracy_knn': accuracy_knn
                  }
                 )


def breast(request):
    # Reading training data set
    df = pd.read_csv('data/Breast_train.csv')
    data = df.values
    X = data[:, :-1]
    Y = data[:, -1]

    # Splitting the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

    # Reading data from user
    value = ''
    accuracy_rf = 0.0
    accuracy_knn = 0.0

    if request.method == 'POST':
        radius = float(request.POST['radius'])
        texture = float(request.POST['texture'])
        perimeter = float(request.POST['perimeter'])
        area = float(request.POST['area'])
        smoothness = float(request.POST['smoothness'])

        # Random Forest Classifier
        rf = RandomForestClassifier(n_estimators=16, criterion='entropy', max_depth=5)
        rf.fit(X_train, y_train)
        y_pred_rf = rf.predict(X_test)
        accuracy_rf = accuracy_score(y_test, y_pred_rf)
        print("Accuracy of Random Forest Classifier:", accuracy_rf*100)


        # K-Nearest Neighbors Classifier
        knn = KNeighborsClassifier(n_neighbors=3)
        knn.fit(X_train, y_train)
        y_pred_knn = knn.predict(X_test)
        accuracy_knn = accuracy_score(y_test, y_pred_knn)
        print("Accuracy of K-Nearest Neighbors Classifier:", accuracy_knn*100)

        user_data = np.array(
            (radius,
             texture,
             perimeter,
             area,
             smoothness)
        ).reshape(1, 5)

        
        # Use the model with the highest accuracy for prediction
        if accuracy_rf >= accuracy_knn:
            predictions = rf.predict(user_data)
        else:
            predictions = knn.predict(user_data)

        if int(predictions[0]) == 1:
            value = 'have'
        elif int(predictions[0]) == 0:
            value = "don't have"

    return render(request,
                  'breast.html',
                  {
                      'context': value
                  }
                 )

def heart(request):
    df = pd.read_csv('data/Heart_train.csv')
    data = df.values
    X = data[:, :-1]
    Y = data[:, -1:]

    value = ''
    accuracy_rf = 0.0
    accuracy_knn = 0.0

    if request.method == 'POST':
        age = float(request.POST['age'])
        sex = float(request.POST['sex'])
        cp = float(request.POST['cp'])
        trestbps = float(request.POST['trestbps'])
        chol = float(request.POST['chol'])
        fbs = float(request.POST['fbs'])
        restecg = float(request.POST['restecg'])
        thalach = float(request.POST['thalach'])
        exang = float(request.POST['exang'])
        oldpeak = float(request.POST['oldpeak'])
        slope = float(request.POST['slope'])
        ca = float(request.POST['ca'])
        thal = float(request.POST['thal'])

        user_data = np.array(
            (age,
             sex,
             cp,
             trestbps,
             chol,
             fbs,
             restecg,
             thalach,
             exang,
             oldpeak,
             slope,
             ca,
             thal)
        ).reshape(1, 13)

        X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

        # Impute missing values with mean
        imputer = SimpleImputer(strategy='mean')
        X_train_imputed = imputer.fit_transform(X_train)
        X_test_imputed = imputer.transform(X_test)
        user_data_imputed = imputer.transform(user_data)

        # Random Forest Classifier
        rf = RandomForestClassifier(n_estimators=16, criterion='entropy', max_depth=9)
        rf.fit(X_train_imputed, y_train)
        y_pred_rf = rf.predict(X_test_imputed)
        accuracy_rf = accuracy_score(y_test, y_pred_rf)

        # K-Nearest Neighbors Classifier
        knn = KNeighborsClassifier(n_neighbors=3)
        knn.fit(X_train_imputed, y_train)
        y_pred_knn = knn.predict(X_test_imputed)
        accuracy_knn = accuracy_score(y_test, y_pred_knn)
        print("Accuracy of Random Forest Classifier:", accuracy_rf*100)
        print("Accuracy of K-Nearest Neighbors Classifier:", accuracy_knn*100)

        if accuracy_rf >= accuracy_knn:
            predictions = rf.predict(user_data_imputed)
        else:
            predictions = knn.predict(user_data_imputed)

        if int(predictions[0]) == 1:
            value = 'positive'
        elif int(predictions[0]) == 0:
            value = "negetive"

    return render(request,
                  'heart.html',
                  {
                      'context': value
                  }
                 )


