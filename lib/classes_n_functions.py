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


## la entrada de esta función es un vector de 18 posiciones
# S-ABC
# Z-ABC
# V-ABC
# VP-ABC
# I- ABC
# IP-ABC
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

    var=np.array([6396379824.971244,
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

    normalized_data=((estado-Mean)/var)

    return Model.predict([normalized_data])