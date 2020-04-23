import pandas as pd
import numpy as np
from sklearn import linear_model
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sb
#%matplotlib inline


hvacs_raw = pd.read_excel( 'tr_hvacs.xlsx')
shows_raw = pd.read_excel('tr_shows.xlsx')

hvacs = hvacs_raw.drop(['h_Qr_Tot'], axis = 1)
shows = shows_raw.drop(['s_Keycode'], axis = 1)

hvacs = hvacs[(hvacs['Date'] >= '2016-09-11') & (hvacs['Date'] < '2018-03-25')]
shows = shows[(shows['Date'] >= '2016-09-11') & (shows['Date'] < '2018-03-25')]

