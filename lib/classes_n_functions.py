import numpy as np
import numpy.fft as fft
import matplotlib.pyplot as plt
class phase:
    def __init__(phase, V, I, Theta_V, Theta_I):
        phase.V=V     
        phase.I=I
        phase.Theta_V=Theta_V
        phase.Theta_I=Theta_I
    
    def mostrar_atributos(phase):
        output =str( "|V|: {} Volts\n|I|: {} Amperes\nTheta_V: {}Â°\nTheta_I: {}Â°".format(
        phase.V, phase.I, phase.Theta_V, phase.Theta_I))
        return(output)


def True_FFT(Voltage,N):
    FFT_VX=(fft.fft(Voltage))
    x=FFT_VX
    x=np.array((x[0:int (N/2+1)])*2/N)
    x[0]=x[0]*2
    FFT_V=x
    return FFT_V    

def True_FFT_phase(Voltages,N):
    FFT_VX=(fft.fft(Voltages,axis=1))
    FFT_V=[]
    for i in range(0,len(FFT_VX)):
        x=FFT_VX[i]
        x=np.array((x[0:int (N/2+1)])*2/N)
        x[0]=x[0]*2
        FFT_V.append(x)
    return FFT_V


def data_Mag(FFT,Z):
    Magnitude=abs(FFT[1*Z]) ##Magnitud de la componente fundamental
    return Magnitude

##Ajustar segun el modelo de adquisiciÃ³n 
def data_angle(FFT1, FFT2,Z):
    Angle=(np.angle(FFT2[1*Z])-np.angle(FFT1[1*Z])) *180/np.pi  ##Fase de la componente funadamental
    return Angle


def update(data, new_data):
    old_data = max(0, len(data) - len(new_data))

    data_update = np.concatenate((data[-old_data:], new_data))
    
    return data_update

def fix_data(data,REF):
        if(data>>31 ==1):
                    data=( data * REF / 0x80000000)-2*REF  
        else:
                    data= (data * REF / 0x7fffffff)   # 32bit
        return data
