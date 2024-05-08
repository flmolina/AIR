from pathlib import Path
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("assets/frame0")
import lib.classes_n_functions as clnf
import numpy as np
import lib.ADS1263 as ADS1263
import time
import joblib
import matplotlib.pyplot as plt
#Inicializacion de cada una de las fases
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

I_Medidor=[1.992, 4.634,2.126]
I_Rele=[0.18,0.43,0.2]
V_Medidor=[127.44,121.54,124.75]
V_Rele=[0.71, 0.72, 0.8]
N=24
REF = 5.08          # Modify according to actual voltage
                    # external AVDD and AVSS(Default), or internal 2.5VModel=joblib.load(relative_to_assets("NN2.joblib"))                    
Model=joblib.load(relative_to_assets("NN2.joblib"))                               
#inicialización del ADC
ADC = ADS1263.ADS1263()
if (ADC.ADS1263_init_ADC1('ADS1263_38400SPS') == -1):
    exit()
ADC.ADS1263_SetMode(0) 


VA_vector=[]
VB_vector=[]
VC_Vector=[]
IA_Vector=[]
IB_Vector=[]
IC_Vector=[]
VAP_Vector=[]
VBP_Vector=[]
VCP_Vector=[]
IAP_Vector=[]
IBP_Vector=[]
ICP_Vector=[]
for i in range(0,100):
    ADC_Data=clnf.get_data(ADC,REF,N)
    FFT=clnf.True_FFT_phase(ADC_Data,24)
    VA=np.round(clnf.data_Mag(FFT[0],3) *(V_Medidor[0]/V_Rele[0]),2)  
    VB=np.round(clnf.data_Mag(FFT[1],3) *(V_Medidor[1]/V_Rele[1]),2)  
    VC=np.round(clnf.data_Mag(FFT[2],3) *(V_Medidor[2]/V_Rele[2]),2) 
    IA=np.round(clnf.data_Mag(FFT[3],3) *(I_Medidor[0]/I_Rele[0]),2)
    IB=np.round(clnf.data_Mag(FFT[4],3) *(I_Medidor[1]/I_Rele[1]),2) 
    IC=np.round(clnf.data_Mag(FFT[5],3) *(I_Medidor[2]/I_Rele[2]),2) 
    VAP=np.round(clnf.data_angle(FFT[0],FFT[0],3),1)
    VBP=np.round(clnf.data_angle(FFT[0],FFT[1],3),1)
    VCP=np.round(clnf.data_angle(FFT[0],FFT[2],3),1)
    IAP=np.round(clnf.data_angle(FFT[0],FFT[3],3),1)
    IBP=np.round(clnf.data_angle(FFT[0],FFT[4],3),1)
    ICP=np.round(clnf.data_angle(FFT[0],FFT[5],3),1)
    Estado=np.array([IA,IB,IC])
    Z=Model.predict(X=[Estado])[0]
    VA_vector.append(VA)
    VB_vector.append(VB)
    VC_Vector.append(VC)
    IA_Vector.append(IA)
    IB_Vector.append(IB)
    IC_Vector.append(IC)
    VAP_Vector.append(VAP)
    VBP_Vector.append(VBP)
    VCP_Vector.append(VCP)
    IAP_Vector.append(IAP)
    IBP_Vector.append(IBP)
    ICP_Vector.append(ICP)


plt.plot(VA_vector)
plt.plot(VB_vector)
plt.plot(VC_Vector)
plt.show()
plt.plot(IA_Vector)
plt.plot(IB_Vector)
plt.plot(IC_Vector)
plt.show()
plt.plot(VAP_Vector)
plt.plot(VBP_Vector)
plt.plot(VCP_Vector)
plt.show()
plt.plot(IAP_Vector)
plt.plot(IBP_Vector)
plt.plot(ICP_Vector)
plt.show()

np.savetxt("Resultado_VA",VA_vector,delimiter=",")
np.savetxt("Resultado_VB",VB_vector,delimiter=",")
np.savetxt("Resultado_VC",VC_Vector,delimiter=",")
np.savetxt("Resultado_IA",IA_Vector,delimiter=",")
np.savetxt("Resultado_IB",IB_Vector,delimiter=",")
np.savetxt("Resultado_IC",IC_Vector,delimiter=",")
np.savetxt("Resultado_VAP",VAP_Vector,delimiter=",")
np.savetxt("Resultado_VBP",VBP_Vector,delimiter=",")
np.savetxt("Resultado_VCP",VCP_Vector,delimiter=",")
np.savetxt("Resultado_IAP",IAP_Vector,delimiter=",")
np.savetxt("Resultado_IBP",IBP_Vector,delimiter=",")
np.savetxt("Resultado_IBP",ICP_Vector,delimiter=",")
