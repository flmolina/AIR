import numpy as np
import numpy.fft as fft

class phase:
    def __init__(phase, V, I, Theta_V, Theta_I):
        phase.V=V     
        phase.I=I
        phase.Theta_V=Theta_V
        phase.Theta_I=Theta_I
    
    def mostrar_atributos(phase):
        print("|V|: "+str(phase.V)+str(" Volts") )
        print("|I|:  " +str(phase.I)+str(" Amperes"))
        print("Theta_V " +str(phase.Theta_V)+str("°") )
        print("Theta_I " +str(phase.Theta_I)+str("°") )

def True_FFT(Voltages,N):
    FFT_VX=(fft.fft(Voltages,axis=1))
    FFT_V=[]
    for i in range(0,len(FFT_VX)):
        x=FFT_VX[i]
        x=np.array((x[0:int (N/2+1)])*2/N)
        x[0]=x[0]*2
        FFT_V.append(x)
    return FFT_V


def data_Mag(FFT):
    Magnitude=abs(FFT[1]) ##Magnitud de la componente fundamental
    return Magnitude

##Ajustar segun el modelo de adquisición 
def data_angle(FFT1, FFT2):
    Angle=(np.angle(FFT2[1])-np.angle(FFT1[1])) *180/np.pi  ##Fase de la componente funadamental
    return Angle


