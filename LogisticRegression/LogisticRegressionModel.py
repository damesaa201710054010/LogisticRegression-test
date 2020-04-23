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
dataframe = pd.read_excel('./inputs/clasificasion.xlsx')
#dataframe.head()
#print(dataframe.head())
#dataframe.describe()
	
#numero de cada categoria
#print(dataframe.groupby('clasificador').size())

#visualizo los datos
#dataframe.drop(['clasificador'],1).hist()
#plt.show()

#grafico de las variables
#sb.pairplot(dataframe.dropna(), hue='clasificador', height=8,vars=["s_TExt_SWC", "s_TExt_NWF","s_Tr_AmbC","s_TRet_AmbF",
#"h_Cap_ChF", "h_Cap_ChC", "h_Cap_Ch1", "h_Cap_Ch2"], kind='reg')

#Eliminacion de datos no necesatios del Data Frame
dataframe1 = dataframe.drop(['Date'], 1)
#Construccion de "X" (independiente) y "y" (dependiente) 
X = np.array(dataframe1.drop(['clasificador'],1))
y = np.array(dataframe['clasificador'])

#comprobacion de dimension
#print(X.shape)
#construccion del modelo de regresion
model = linear_model.LogisticRegression()
model.fit(X,y)
#Prediccion acorde a los datos anteriores
predictions = model.predict(X)
print(predictions)#[0:5]
#print(dataframe['clasificador'])
print(model.score(X,y))
