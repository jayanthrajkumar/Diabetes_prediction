# -*- coding: utf-8 -*-
"""diabetes_prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lFuJ34OOBO8zHQENHfDaxKAXRSxevPwG
"""

from google.colab import drive
drive.mount("/content/drive")

# Importing libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings('ignore')

path='/content/drive/MyDrive/datasets/diabetes_prediction_dataset.csv'

# Importing dataset
dataset = pd.read_csv(path)

# Preview data
dataset.head()

# Dataset dimensions - (rows, columns)
dataset.shape

# Features data-type
dataset.info()

# Statistical summary
dataset.describe().T

# Count of null values
dataset.isnull().sum()

# Outcome countplot
sns.countplot(x = 'diabetes',data = dataset)

# Histogram of each feature
import itertools

col = dataset.columns[:8]
plt.subplots(figsize = (20, 15))
length = len(col)

for i, j in itertools.zip_longest(col, range(length)):
    plt.subplot((length//2), 3, j + 1)
    plt.subplots_adjust(wspace = 0.1,hspace = 0.5)
    dataset[i].hist(bins = 20)
    plt.title(i)
plt.show()

# Scatter plot matrix
from pandas.plotting import scatter_matrix
scatter_matrix(dataset, figsize = (20, 20));

# Pairplot
sns.pairplot(data = dataset, hue = 'diabetes')
plt.show()

dataset = pd.get_dummies(dataset, drop_first=True)

sns.heatmap(dataset.corr(), annot=True)
plt.show()

dataset_new = dataset

columns_to_replace = ["bmi", "HbA1c_level", "blood_glucose_level"]
dataset[columns_to_replace] = dataset[columns_to_replace].replace(0, np.NaN)

# Count of NaN
dataset_new.isnull().sum()

# Statistical summary
dataset_new.describe().T

# Feature scaling using MinMaxScaler
from sklearn.preprocessing import MinMaxScaler
sc = MinMaxScaler(feature_range = (0, 1))
dataset_scaled = sc.fit_transform(dataset_new)

dataset_scaled = pd.DataFrame(dataset_scaled)

# Selecting features - [Glucose, Insulin, BMI, Age]
X = dataset_scaled.iloc[:, [1, 4, 5, 7]].values
Y = dataset_scaled.iloc[:, 8].values

# Splitting X and Y
from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.20, random_state = 42, stratify = dataset_new['diabetes'])

# Checking dimensions
print("X_train shape:", X_train.shape)
print("X_test shape:", X_test.shape)
print("Y_train shape:", Y_train.shape)
print("Y_test shape:", Y_test.shape)

# Logistic Regression Algorithm
from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression(random_state = 42)
logreg.fit(X_train, Y_train)

import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Select relevant features and target variable
# Replace "your_target_column" with the actual target column in your dataset, e.g., "diabetes"
X = dataset.drop(columns=['diabetes'])  # Adjust this based on your target column name
Y = dataset['diabetes']

# Convert categorical features to numerical if necessary
X = pd.get_dummies(X, drop_first=True)

# Split the dataset into training and testing sets
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

# Scale the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Define the range for n_neighbors values
X_axis = list(range(1, 31))
acc = pd.Series(dtype="float")  # Initialize an empty Series to store accuracy values

# Loop through each n_neighbors value to train and evaluate the model
for i in range(1, 31):
    knn_model = KNeighborsClassifier(n_neighbors=i)
    knn_model.fit(X_train_scaled, Y_train)
    prediction = knn_model.predict(X_test_scaled)
    acc.loc[i] = metrics.accuracy_score(prediction, Y_test)  # Store accuracy for each n_neighbors

# Plot the accuracy vs. n_neighbors
plt.plot(X_axis, acc)
plt.xticks(X_axis)
plt.title("Finding Best Value for n_neighbors")
plt.xlabel("n_neighbors")
plt.ylabel("Accuracy")
plt.grid()
plt.show()

print('Highest Accuracy Value:', acc.values.max())

# K nearest neighbors Algorithm
from sklearn.neighbors import KNeighborsClassifier
knn = KNeighborsClassifier(n_neighbors = 24, metric = 'minkowski', p = 2)
knn.fit(X_train, Y_train)

# Support Vector Classifier Algorithm
from sklearn.svm import SVC
svc = SVC(kernel = 'linear', random_state = 42)
svc.fit(X_train, Y_train)

# Naive Bayes Algorithm
from sklearn.naive_bayes import GaussianNB
nb = GaussianNB()
nb.fit(X_train, Y_train)

# Decision tree Algorithm
from sklearn.tree import DecisionTreeClassifier
dectree = DecisionTreeClassifier(criterion = 'entropy', random_state = 42)
dectree.fit(X_train, Y_train)

# Random forest Algorithm
from sklearn.ensemble import RandomForestClassifier
ranfor = RandomForestClassifier(n_estimators = 11, criterion = 'entropy', random_state = 42)
ranfor.fit(X_train, Y_train)

# Ensure consistent preprocessing for training and test datasets
X = dataset.drop(columns=['diabetes'])  # Replace 'diabetes' with your target column
Y = dataset['diabetes']

# Convert categorical variables to numeric
X = pd.get_dummies(X, drop_first=True)

# Split dataset
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

# Scale data
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train models
logreg = LogisticRegression().fit(X_train, Y_train)
knn = KNeighborsClassifier(n_neighbors=5).fit(X_train, Y_train)
svc = SVC().fit(X_train, Y_train)
nb = GaussianNB().fit(X_train, Y_train)
dectree = DecisionTreeClassifier().fit(X_train, Y_train)
ranfor = RandomForestClassifier().fit(X_train, Y_train)

# Make predictions
Y_pred_logreg = logreg.predict(X_test)
Y_pred_knn = knn.predict(X_test)
Y_pred_svc = svc.predict(X_test)
Y_pred_nb = nb.predict(X_test)
Y_pred_dectree = dectree.predict(X_test)
Y_pred_ranfor = ranfor.predict(X_test)

# Evaluating using accuracy_score metric
from sklearn.metrics import accuracy_score
accuracy_logreg = accuracy_score(Y_test, Y_pred_logreg)
accuracy_knn = accuracy_score(Y_test, Y_pred_knn)
accuracy_svc = accuracy_score(Y_test, Y_pred_svc)
accuracy_nb = accuracy_score(Y_test, Y_pred_nb)
accuracy_dectree = accuracy_score(Y_test, Y_pred_dectree)
accuracy_ranfor = accuracy_score(Y_test, Y_pred_ranfor)

# Accuracy on test set
print("Logistic Regression: " + str(accuracy_logreg * 100))
print("K Nearest neighbors: " + str(accuracy_knn * 100))
print("Support Vector Classifier: " + str(accuracy_svc * 100))
print("Naive Bayes: " + str(accuracy_nb * 100))
print("Decision tree: " + str(accuracy_dectree * 100))
print("Random Forest: " + str(accuracy_ranfor * 100))

# Confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(Y_test, Y_pred_knn)
cm

# Heatmap of Confusion matrix
sns.heatmap(pd.DataFrame(cm), annot=True)

# Classification report
from sklearn.metrics import classification_report
print(classification_report(Y_test, Y_pred_knn))