import numpy as np
import joblib
import sklearn
import time
import matplotlib.pyplot as plt
Model=joblib.load("NN1.joblib")

"[[ 3177    87]"
"[   86 16650]]"

def predict(data,Model):
    return Model.predict_proba(X=[data])

for i in range(0,100,1):
    z=1+(i/100)
    Normal=          np.array([ 3.74*z,
                                4.94*z,
                                2.31*z])
    
    inicio=time.time()
    Y=predict(Normal,Model)[0][1]
    final=time.time()
    #print("Corriente al "+str(np.round((z*100),1))+str("%= ")   +str(Y))
    print(str((final-inicio)*1000))



