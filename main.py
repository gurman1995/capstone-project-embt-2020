import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from keras.preprocessing.sequence import pad_sequences
from joblib import dump, load
import numpy as np
target = os.listdir("Data")

training_data = []
training_target = []
max_length = 150
for j in target:
    for i in range(10):
        data = pd.read_csv(f'Data/{j}/{i}.csv', index_col=False)
        data = data.values.flatten()
        training_data.append(data)
        training_target.append(j)
padded = pad_sequences(training_data, padding="post", maxlen=150)
x_train, x_test, y_train, y_test = train_test_split(padded, training_target)
clf = RandomForestClassifier()
clf.fit(padded, training_target)
#print(x_train[0].tolist())
dump(clf, 'model.joblib')
