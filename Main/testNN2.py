
import numpy as np
import joblib
import sklearn
import time
import os
Model=joblib.load("NN2.joblib")


def predict(data,Model):

    Mean=np.array([1118482.007198,
                   2007257.300996,
                   1190185.479724,
                   41.085172     ,
                   39.644329     ,
                   75.761703     ,
                   672.680633    ,
                   919.997673    ,
                   689.814087    ,
                   0.264774      ,
                   0.129744      ,
                   -0.111289     ,
                   43.130137     ,
                   50.639194     ,
                   43.322110     ,
                   0.013401      ,
                   0.490339      ,
                   -0.226805     ])

    std=np.array([352084066635350.562500,
                1155241187992597.75000,
                400182719390413.750000,
                1049.240836,
                6083.239196,
                49836.176135,
                15778063.143528,
                34407636.604695,
                17237973.151341,
                3.977480,
                2.997568,
                2.759565,
                75614.147792,
                111999.672710,
                78532.361840,
                4.148813,
                2.568966,
                3.588052])

    normalized_data=((data-Mean)/np.sqrt(std))
    return Model.predict(X=[normalized_data])

Falla=np.array([ 1103, #VA
                1237, #VA
                862, ##VA
                (121.56)/2,      #Ohms
                (127)/3.8,    #Ohms
                (123.11)/1.85,   #Ohms
                121.56,          #Volts
                127,          #Volts
                123,          #Volts
                np.deg2rad(-1)       ,
                np.deg2rad(-121)    ,
                np.deg2rad(119)     ,
                9,          #Amperes          
                9.7,          #Amperes
                6.9,          #Amperes
                np.deg2rad(7)   ,
                np.deg2rad(-131)    ,
                np.deg2rad(-103)  ])



Normal=          np.array([ 74, #VA
                72, #VA
                70, ##VA
                (121)/2,      #Ohms
                (127)/3.8,    #Ohms
                (123)/1.85,   #Ohms
                122.56,          #Volts
                123,          #Volts
                123,          #Volts
                np.deg2rad(-0.24)       ,
                np.deg2rad(-120)    ,
                np.deg2rad(120)     ,
                2,          #Amperes          
                3.8,          #Amperes
                1.85,          #Amperes
                np.deg2rad(86)   ,
                np.deg2rad(-32)    ,
                np.deg2rad(-153)  ])



X=predict(Falla,Model)[0]
Y=predict(Normal,Model)[0]
print("condición de Falla " +str(X))
print("condición Normal "   +str(Y))