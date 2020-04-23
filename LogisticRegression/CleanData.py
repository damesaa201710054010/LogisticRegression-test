import pandas as pd
import numpy as np
from pandas import ExcelWriter
from sklearn import linear_model
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sb
#%matplotlib inline

hvacs_raw = pd.read_excel('./input/tr_hvacs.xlsx')
shows_raw = pd.read_excel('./input/tr_shows.xlsx')

hvacs =   hvacs_raw[
    ['Date',
    'h_Cap_Ch1', 
    'h_Cap_Ch2', 
    'h_Cap_ChC', 
    'h_Cap_ChF'
    ]
]                             
shows = shows_raw.drop(['s_Keycode'], axis = 1)

#Selecciona el periodo de observacion
hvacs = hvacs[(hvacs['Date'] >= '2016-09-11') & (hvacs['Date'] < '2017-05-01')]
shows = shows[(shows['Date'] >= '2016-09-11') & (shows['Date'] < '2017-05-01')]

#writer = ExcelWriter('s1.xlsx')
#hvacs.to_excel(writer, 'Hoja de datos', index=False)
#writer.save()

#Remueve ceros
hvacs = hvacs.loc[:, (hvacs != 0).any(axis = 0)]
shows = shows.loc[:, (shows != 0).any(axis = 0)]

"""writer = ExcelWriter('s.xlsx')
shows.to_excel(writer, 'Hoja de datos', index=False)
writer.save()"""

#Organiza por fecha y elimina duplicaciones
shows = shows.sort_values(by=['Date'])
shows = shows.drop_duplicates(['Date'])


#Date como index para remuestreo
hvacs = hvacs.set_index(['Date'])
shows = shows.set_index(['Date'])

#Re-sampling to 15min & re-filling, with linear interpolation
idx = pd.date_range('2016-09-11', '2018-03-24 23:45', freq = '15T')
hvacs = hvacs.reindex(idx).interpolate(method = 'linear')
shows = shows.reindex(idx).fillna(method = 'pad', limit = 1)

#  Merging tables in one data frame, 'df'
df = pd.DataFrame()
df = hvacs.merge(shows, left_index = True, right_index = True)
#df = shows.merge(shows, left_index = True, right_index = True)

#  Recovering 'Date' as data with new name, 'tStart'
df = df.reset_index()
df = df.rename(columns = {'index':'tStart'})

df['clasificador'] = 1

df1 = pd.DataFrame()
hvacsAux = pd.DataFrame()

sumHot= 0
sumCool = 0
sumZones = 0
averageZones = 0

for indice_fila, fila in df.iterrows():
    if(indice_fila == 0):
        sumCool = fila['h_Cap_Ch1'] + fila['h_Cap_Ch2']  
        sumHot = fila['h_Cap_ChC'] + fila['h_Cap_ChF']
        sumZones = (fila['s_Tr_AmbC'] +
                   fila['s_Tr_CrcC'] +
                    fila['s_Tr_CrcF'] + 
                    fila['s_Tr_FyrF'] +
                    fila['s_Tr_GdF'] + 
                    fila['s_Tr_GoyaF'] + 
                    fila['s_Tr_Hal1F'] + 
                    fila['s_Tr_PitF'] + 
                    fila['s_Tr_StdsC'] + 
                    fila['s_Tr_StdsF'] +
                    fila['s_TRet_AmbF'] + 
                    fila['s_TRet_StllC'] + 
                    fila['s_TRet_StllF']) 
        averageZones = sumZones / 13
    if(indice_fila >= 1):
        print("hi")
        sumZonesTimeT= (fila['s_Tr_AmbC'] +
                   fila['s_Tr_CrcC'] +
                    fila['s_Tr_CrcF'] + 
                    fila['s_Tr_FyrF'] +
                    fila['s_Tr_GdF'] + 
                    fila['s_Tr_GoyaF'] + 
                    fila['s_Tr_Hal1F'] + 
                    fila['s_Tr_PitF'] + 
                    fila['s_Tr_StdsC'] + 
                    fila['s_Tr_StdsF'] +
                    fila['s_TRet_AmbF'] + 
                    fila['s_TRet_StllC'] + 
                    fila['s_TRet_StllF'])
        averageZonesTimeT = sumZonesTimeT / 13
        if(sumCool > sumHot):
            if(averageZonesTimeT >= averageZones):
                fila['clasificador'] = 0
        else:
            if(averageZonesTimeT <= averageZones):
                fila['clasificador'] = 0

        sumCool = fila['h_Cap_Ch1'] + fila['h_Cap_Ch2']  
        sumHot = fila['h_Cap_ChC'] + fila['h_Cap_ChF']
        averageZones = averageZonesTimeT


writer = ExcelWriter('clasificasion.xlsx')
df.to_excel(writer, 'Hoja de datos', index=False)
writer.save()
