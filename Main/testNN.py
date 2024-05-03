import numpy as np
import joblib
import sklearn
import time
Model=joblib.load("NN.joblib")


def predict(estado,Model):
    Mean=np.array([5839.074220,
    7061.736407,
    4902.503453,
    38.128003  ,
    47.863958  ,
    68.348688  ,
    153.001569 ,
    156.524264 ,
    146.806856 ,
    0.293765   ,
    0.188813   ,
    -0.062767  ,
    7.482766   ,
    7.604663   ,
    7.080138   ,
    -0.217297  ,
    0.558062   ,
    -0.290082  ])

    std=np.array([6396379824.971244,
        9405516053.802622,
        4360129360.965660,
        349.518481,
        1746351.907888,
        89135.605438,
        102039.080906,
        133339.606473,
        79522.579804,
        4.072448,
        3.096451,
        2.802325,
        337.582695,
        368.279829,
        375.622753,
        4.080932,
        2.577789,
        3.128683])

    normalized_data=((estado-Mean)/std)
    return Model.predict(X=[normalized_data])

data=np.array([ 586.6, #VA
                735.3, #VA
                409.7, ##VA
                (119.65)/4.922,  #Ohms
                (120.62)/6.184,  #Ohms
                (117.74)/3.523,  #Ohms
                119.65,          #Volts
                120.62,          #Volts
                117.74,          #Volts
                np.deg2rad(0)       ,
                np.deg2rad(-121)    ,
                np.deg2rad(121)     ,
                4.922,          #Amperes          
                6.184,          #Amperes
                3.523,          #Amperes
                np.deg2rad(-171)   ,
                np.deg2rad(46)    ,
                np.deg2rad(-83)  ])
X=predict(data,Model)[0]
print(X)