import numpy as np
import numpy.fft as fft
import lib.ADS1263 as ADS1263
import RPi.GPIO
class phase:
    def __init__(phase, V, I):
        phase.V=V     
        phase.I=I
        phase.S=V*I
        phase.Z=V/I
    
    def mostrar_atributos(phase):
        output =str( "V,rms: {} Volts\nI,rms: {} Amperes\nS: {}VA\nZ: {}Ohms".format(
        np.round(phase.V,2), np.round(phase.I,2), np.round(phase.S,2), np.round(phase.Z,2)))
        return(output)


def True_FFT(Voltage,N):
    FFT_VX=(fft.fft(Voltage))
    x=FFT_VX
    x=np.array((x[0:int (N/2+1)])*2/N)
    x[0]=x[0]*2
    FFT_V=x
    return FFT_V    

def True_FFT_phase(Data,N):
    FFT_VX=(fft.fft(Data,axis=1))
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
    Angle=(np.angle(FFT2[1*Z])-np.angle(FFT1[1*Z])) *180/np.pi
    Angle=(Angle+180) % 360 - 180  ##Fase de la componente funadamental
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


def get_data(ADC,REF,N):
    ADC_Values=[[],[],[],[],[],[]]
    for i in range (0,N):
            ADC_Values[0].append(fix_data(ADC.ADS1263_GetChannalValue(0),REF))
            ADC_Values[1].append(fix_data(ADC.ADS1263_GetChannalValue(1),REF))
            ADC_Values[2].append(fix_data(ADC.ADS1263_GetChannalValue(2),REF))
            ADC_Values[3].append(fix_data(ADC.ADS1263_GetChannalValue(3),REF))
            ADC_Values[4].append(fix_data(ADC.ADS1263_GetChannalValue(4),REF))
            ADC_Values[5].append(fix_data(ADC.ADS1263_GetChannalValue(5),REF))
    return ADC_Values

def RMS(data):
      data-=np.mean(data)# eliminar la componente DC del RMS
      return np.sqrt(np.mean(np.square(data)))

       
