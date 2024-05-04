import numpy as np
import joblib
import sklearn
import time
Model=joblib.load("NN.joblib")


def predict(data,Model):
    Mean=np.array([5839.074220,7061.736407,
                   4902.503453,38.128003  ,47.863958  
                   ,68.348688  ,153.001569 ,156.524264 
                   ,146.806856 ,0.293765   ,0.188813   
                   ,-0.062767  ,7.482766   ,7.604663   
                   ,7.080138   ,-0.217297  ,0.558062   
                   ,-0.290082  ])/1000

    std=np.array([6396379824.971244,9405516053.802622,4360129360.965660,349.518481,
                  1746351.907888,89135.605438,102039.080906,133339.606473,79522.579804,
                  4.072448,3.096451,2.802325,337.582695,368.279829,375.622753,4.080932,2.577789,
                  3.128683])/10000

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


z=1.6
Normal=          np.array([ 427, #VA
                625, #VA
                286, ##VA
                (122)/(3.7*z),      #Ohms
                (127)/(4.8*z),    #Ohms
                (124)/(2.3*z),   #Ohms
                122,          #Volts
                127,          #Volts
                124,          #Volts
                np.deg2rad(-0.24)       ,
                np.deg2rad(-120)    ,
                np.deg2rad(120)     ,
                3.7*z,          #Amperes          
                4.8*z,          #Amperes
                2.3*z,          #Amperes
                np.deg2rad(16)   ,
                np.deg2rad(-141)    ,
                np.deg2rad(64)  ])





X=predict(Falla,Model)[0]
Y=predict(Normal,Model)[0]
print("condición de Falla " +str(X))
print("condición Normal "   +str(Y))