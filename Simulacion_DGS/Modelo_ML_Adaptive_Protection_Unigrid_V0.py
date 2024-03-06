# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 11:06:05 2021

@author: juang
"""

import pandas as pd
import numpy as np
import math
from joblib import load
from os import scandir
import matplotlib.pyplot as plt
import scipy.io 

def get_measures(X1,Xd1,Xs1,Lin):
    Reles1=np.zeros((np.size(X1,0),6))
    Reles2=np.zeros((np.size(X1,0),6))
    #Convertir Lin en Li,LF,No1 y No2
    Li=Lin[0:4]
    Lf=Lin[4:8]
    No1=("N%s" %(Lin[1:4]))
    No2=("N%s" %(Lin[5:8]))
    # Se obtienen los IEDs asociados a la línea
    pt=0
    IED=np.zeros(2)
    for i in range(np.size(Xs1,0)):
        if str(Xs1[i,1])==No1[1:4] and (str(Xs1[i,2])==No2[1:4] or str(Xs1[i,3])==No2[1:4]): 
           IED[pt]=Xs1[i,0]# obtiene los IEDs asociados a la línea a analizar
           pt=pt+1
    islin=0
    for kl in range(np.size(Xd1)):
        if len(Xd1[kl])>3:
           if Li==Xd1[kl][0:4]:
              Sequal=1
           else:
              Sequal=0  
           if Lf==Xd1[kl][len(Xd1[kl])-4:len(Xd1[kl])]:
              Sequax=1
           else:
              Sequax=0
           if No1==Xd1[kl]:
              Sequal1=1
           else:
              Sequal1=0  
           if No2==Xd1[kl]:
              Sequal2=1
           else:
              Sequal2=0  
        else:
           if Li==Xd1[kl][0:3]:
              Sequal=1
           else:
              Sequal=0  
           if Lf==Xd1[kl][len(Xd1[kl])-3:len(Xd1[kl])]:
              Sequax=1
           else:
              Sequax=0
           if No1==Xd1[kl]:
              Sequal1=1
           else:
              Sequal1=0  
           if No2==Xd1[kl]:
              Sequal2=1
           else:
              Sequal2=0 
        if Sequal==1:
           Poscor=kl
           islin=1
        if Sequax==1:
           Poscorx=kl
           islin=1
        if Sequal1==1:
           Posten1=kl
        if Sequal2==1:
           Posten2=kl
    if islin==1:
    #LLenar la matriz de datos vector
       for kp in range(np.size(X1,0)):
           Reles1[kp,0:3]=X1[kp,Posten1-2:Posten1+1]
       if Poscor==Poscorx:
          for kp in range(np.size(X1,0)): 
              Reles1[kp,3:6]=X1[kp,Poscor-5:Poscor-2]
       else:
          for kp in range(np.size(X1,0)): 
              Reles1[kp,3:6]=X1[kp,Poscor-2:Poscor+1] 
       for kp in range(np.size(X1,0)):
           Reles2[kp,0:3]=X1[kp,Posten2-2:Posten2+1]
       for kp in range(np.size(X1,0)):
           Reles2[kp,3:6]=X1[kp,Poscorx-2:Poscorx+1]
    else:
       for kp in range(np.size(X1,0)):
           Reles1[kp,0:3]=X1[kp,Posten1-2:Posten1+1]
       Reles1[kp,3:6]=np.zeros((np.size(X1,0),3))
       for kp in range(np.size(X1,0)):
           Reles2[kp,0:3]=X1[kp,Posten2-2:Posten2+1]
       Reles2[kp,3:6]=np.zeros((np.size(X1,0),3)) 
    return Reles1, IED, Reles2

# Función para obtener los atributos por la ventana propuesta
def getatri(V,I,P,MEME,MEDES):
    pomE=[0,1,2,6,7,8,9,10,11,12,13,14,15,16,17]
    VI=np.zeros((2*P,6))    
    #Ainv=np.array([[1,1,1],[1,complex(-0.5,0.866025),complex(-0.5,-0.866025)],[1,complex(-0.5,-0.866025),complex(-0.5,0.866025)]])
    VI[:,0:3]=V[:,0:3]
    VI[:,3:6]=I[:,0:3]
    VIf=np.zeros((2*P,6),dtype=complex)
    for ky in range(6):
        VIfx=np.fft.fft(VI[:,ky])
        VIf[:,ky]=VIfx
    #temp=np.max(np.abs(VIf[0:P/2,6]))
    pos=np.argmax(np.abs(VIf[0:int(P),4]))
    VIfinal=VIf[pos,:]/P
    V1=VIfinal[0:3]
    I1=VIfinal[3:6]
    Vmag=np.abs(V1)/math.sqrt(2)
    Imag=np.abs(I1)/math.sqrt(2)
    Vang=np.angle(V1)
    Iang=np.angle(I1)
    #Vsec=np.dot((0.33333333)*Ainv,(0.707106)*V1[3:6])
    #Isec=np.dot((0.33333333)*Ainv,(0.707106)*I1[3:6])
    #Vsecpre=np.dot((0.33333333)*Ainv,(0.707106)*V1[0:3])
    #Isecpre=np.dot((0.33333333)*Ainv,(0.707106)*I1[0:3])
    des=np.zeros((1,18))
    # des[0,0]=np.abs(Vsec[0])
    # des[0,1]=np.angle(Vsec[0])
    # des[0,2]=np.abs(Vsec[2])
    # des[0,3]=np.angle(Vsec[2])
    # des[0,4]=np.abs(Isec[0])
    # des[0,5]=np.angle(Isec[0])
    # des[0,6]=np.abs(Isec[2])
    # des[0,7]=np.angle(Isec[2])
    ## Determinar la potenia
    temp=np.zeros((1,3))
    temp1=np.zeros((1,3))
    for k in range(3):
        temp[0,k]=Vmag[k]*Imag[k]#Potencia
        temp1[0,k]=Vmag[k]/Imag[k]#Impedancia
    des[0,0:3]=temp[0,0:3]
    des[0,3:6]=temp1[0,0:3]
    des[0,6:9]=Vmag[0:3]
    des[0,9:12]=Vang[0:3]
    des[0,12:15]=Imag[0:3]
    des[0,15:18]=Iang[0:3]
    
    des1F=np.zeros((1,18))
    des1F1=np.zeros((1,18))
    des1F[0,0]=des[0,0]
    des1F[0,1]=des[0,1]
    des1F[0,2]=des[0,2]
    des1F[0,3]=des[0,3]
    des1F[0,4]=des[0,4]
    des1F[0,5]=des[0,5]
    des1F[0,6]=des[0,6]
    des1F[0,7]=des[0,7]
    des1F[0,8]=des[0,8]
    des1F[0,9]=des[0,9]
    des1F[0,10]=des[0,10]
    des1F[0,11]=des[0,11]
    des1F[0,12]=des[0,12]
    des1F[0,13]=des[0,13]
    des1F[0,14]=des[0,14]
    des1F[0,15]=des[0,15]
    des1F[0,16]=des[0,16]
    des1F[0,17]=des[0,17]

    
    #################################################################
 
    des1F1[0,0]=des1F[0,0]*1000000
    des1F1[0,1]=des1F[0,1]*1000000
    des1F1[0,2]=des1F[0,2]*1000000
    des1F1[0,3]=des1F[0,3]
    des1F1[0,4]=des1F[0,4]
    des1F1[0,5]=des1F[0,5]
    des1F1[0,6]=des1F[0,6]*1000
    des1F1[0,7]=des1F[0,7]*1000
    des1F1[0,8]=des1F[0,8]*1000
    des1F1[0,9]=des1F[0,9]
    des1F1[0,10]=des1F[0,10]
    des1F1[0,11]=des1F[0,11]
    des1F1[0,12]=des1F[0,12]*1000
    des1F1[0,13]=des1F[0,13]*1000
    des1F1[0,14]=des1F[0,14]*1000
    des1F1[0,15]=des1F[0,15]
    des1F1[0,16]=des1F[0,16]
    des1F1[0,17]=des1F[0,17]

    
    for ki in range(np.size(pomE)):
        des1F[0,ki]=(des1F1[0,ki]-MEME[pomE[ki]])/(np.sqrt(MEDES[pomE[ki]]))
    return des1F, des1F1

## Información de entrada para encontrar los datos 
MFNF=1# 1 significa datos de falla 0 significa datos de no falla
Sys=13#Elige la red a analizar IEEE34 o IEEE123
Topo=0;# Tiene en cuenta las topologias del sistema 0:Original
SalGen=1#Salida de Generador del sistema 0:Sin salida de generadores
VarCar=4# Variación de carga 2: Carga 110%
Resfal=35#Resistencia de falla 0:Sólida a tierra
Lin="L650-632"#Nombre de la línea en falla
Dfuen=4
ECA=0#Switcheo de capacitores
TiFal=0# Tipo de falla 0:Trifásica




## La primera parte leera el archivo de las muestras y mostrará la señal en el tiempo
Fmu=1920#Frecuencia de muestreo a las que se ebtuvieron las señales (Generalmente es fijo este valor)
ts=0.1#tiempo de duración de la simulación
tf=0.05#tiempo de ocurrencia de la falla
#Cargar el archivo .cvs que se quiere evaluar (Se podrian cargar una serie de archivos)
#Determinar si es de falla o no falla

MOP=1# Tipo de datos a obtener 1 Test primario o test secundario
#IED=1#Se selecciona el dispositivo a analizar
MPC=32#Tamaño de la ventana, 2 ciclos (Número de muestras por ciclo 128)
StW=4#Paso de la ventana,1 ciclo

#

def ls2(path): #Sirve para listar los archivos de una carpeta
    return [obj.name for obj in scandir(path) if obj.is_file()]


if Sys==13:
    #Cargar los archivos de medias y desviaciones en .csv  
    #MN=pd.read_csv("medias_REles_IEEE34.csv")
    dirrt12=pd.read_csv("IUnigrid_MeanVar_V10_App2_18F_0.csv",header=None,sep=",")
    MN=dirrt12.iloc[0:np.size(dirrt12,0),0].values
    Sd=dirrt12.iloc[0:np.size(dirrt12,0),1].values
    if MFNF==1:
        dirrt=pd.read_csv("Escenarios_Falla_Unigrid_falla_V3.csv",sep=",")
        Esce=dirrt.iloc[0:np.size(dirrt,0),:].values
        bad=0
        for kh in range(np.size(dirrt,0)):
            if Esce[kh,0]==Topo:
               bad=bad+1
            if Esce[kh,1]==SalGen:
               bad=bad+1
            if Esce[kh,2]==VarCar:
               bad=bad+1
            if Esce[kh,3]==Resfal:
               bad=bad+1
            if Esce[kh,4]==Lin:
               bad=bad+1
            if Esce[kh,5]==ECA:
               bad=bad+1
            if Esce[kh,6]==TiFal:
               bad=bad+1
            if bad==7:
               posu=kh
               break 
            bad=0
        if len(str(posu))==1:
           pyl=("UnigridRD00%s"%(str(posu)))
        else:
           pyl=("UnigridRD0%s"%(str(posu))) 
        pyl1=".csv"
        pyl2=pyl+pyl1
        direc=ls2("D:\CSV_digsilent_Falla_Unigrid_V3")
        Tar=len(direc)
        for kj in range(Tar):
            if pyl2==direc[kj]:
               direc1=direc[kj]
               print(direc1)
               Att=("D:\CSV_digsilent_Falla_Unigrid_V3\\")
               AS=Att+direc1
               fid=pd.read_csv(AS,header=None,sep=";")
               X1=fid.iloc[2:195,:].values
               Xd1=fid.iloc[0,:].values
               dirto=pd.read_csv("Reles_Unigrid.csv",sep=";")
               XIED=dirto.iloc[0:np.size(dirto,0),:].values
    elif MFNF==0:
        dirrt=pd.read_csv("Escenarios_Falla_Unigrid_No_falla_V2.csv",sep=",")
        Esce=dirrt.iloc[0:np.size(dirrt,0),:].values
        bad=0
        for kh in range(np.size(dirrt,0)):
            if Esce[kh,0]==Topo:
               bad=bad+1
            if Esce[kh,1]==SalGen:
               bad=bad+1
            if Esce[kh,2]==ECA:
               bad=bad+1   
            if Esce[kh,3]==VarCar:
               bad=bad+1
            if bad==4:
               posu=kh
               break 
            bad=0
        if len(str(posu))==1:
           pyl=("UnigridRD00%s"%(str(posu)))
        else:
           pyl=("UnigridRD0%s"%(str(posu))) 
        pyl1=".csv"
        pyl2=pyl+pyl1       
        direct=ls2("D:\CSV_digsilent_No_Falla_Unigrid_V2")
        Tar=len(direct) 
        for kj in range(Tar):
            if pyl2==direct[kj]:
               direc1=direct[kj]
               print(direc1)
               Att=("D:\CSV_digsilent_No_Falla_Unigrid_V2\\")
               AS=Att+direc1
               fid=pd.read_csv(AS,header=None,sep=";")
               X1=fid.iloc[2:195,:].values
               Xd1=fid.iloc[0,:].values
               dirto=pd.read_csv("Reles_Unigrid.csv",sep=";")
               XIED=dirto.iloc[0:np.size(dirto,0),:].values
# elif Sys==123:
#       #Cargar los archivos de medias y desviaciones en .csv  
#     MN=scipy.io.loadmat("medias_REles_IEEE123.csv")
#     Sd=scipy.io.loadmat("desviaciones_REles_IEEE123.csv") 
#     if MFNF==1:
#         dirrt=pd.read_csv("Datos_IEEE123\Escenarios_Falla_Distancia_IEEE123.csv",sep=";")
#         Esce=dirrt.iloc[0:np.size(dirrt,0),:].values
#         bad=0
#         for kh in range(np.size(dirrt,0)):
#             if Esce[kh,0]==Topo:
#                bad=bad+1
#             if Esce[kh,1]==SalGen:
#                bad=bad+1
#             if Esce[kh,2]==VarCar:
#                bad=bad+1
#             if Esce[kh,3]==Resfal:
#                bad=bad+1
#             if Esce[kh,4]==Lin:
#                bad=bad+1
#             if Esce[kh,5]==ECA:
#                bad=bad+1
#             if Esce[kh,6]==TiFal:
#                bad=bad+1
#             if bad==7:
#                posu=kh
#                break 
#             bad=0
#         if np.size(str(posu))==1:
#            pyl=("juanRD00%s"%(str(posu)))
#         pyl1=".csv"
#         pyl2=pyl+pyl1
#         direc=ls2("D:\CSV_digsilent_Falla_Distancia_RDF_IEEE123")
#         Tar=len(direc)
#         for kj in range(Tar):
#             if pyl2==direc[kj]:
#                direc1=direc[kj]
#                print(direc1)
#                Att=("D:\CSV_digsilent_Falla_Distancia_RDF_IEEE123")
#                AS=Att+direc1
#                fid=pd.read_csv(AS,header=None)
#                X1=fid.iloc[2:771,:].values
#                Xd1=fid.iloc[0,:].values
#                dirto=pd.read_csv("Datos_IEEE123\Reles_IEEE123_34IEDS+",sep=";")
#                XIED=dirto.iloc[0:np.size(dirto,0),:].values
#     elif MFNF==0:
#         dirrt=pd.read_csv("Datos_IEEE123\Escenarios_NoFalla_IEEE123.csv",sep=";")
#         Esce=dirrt.iloc[0:np.size(dirrt,0),:].values
#         bad=0
#         for kh in range(np.size(dirrt,0)):
#             if Esce[kh,0]==Topo:
#                bad=bad+1
#             if Esce[kh,1]==SalGen:
#                bad=bad+1
#             if Esce[kh,2]==VarCar:
#                bad=bad+1
#             if bad==3:
#                posu=kh
#                break 
#             bad=0
#         if np.size(str(posu))==1:
#            pyl=("juanRD00%s"%(str(posu)))
#         pyl1=".csv"
#         pyl2=pyl+pyl1
#         direc=ls2("D:\CSV_digsilent_Sin_Falla_RDF_IEEE123\\")
#         Tar=len(direc)
#         for kj in range(Tar):
#             if pyl2==direc[kj]:
#                direc1=direc[kj]
#                print(direc1)
#                Att=("D:\CSV_digsilent_Sin_Falla_RDF_IEEE123\\")
#                AS=Att+direc1
#                fid=pd.read_csv(AS,header=None)
#                X1=fid.iloc[2:771,:].values
#                Xd1=fid.iloc[0,:].values
#                dirto=pd.read_csv("Datos_IEEE123\Reles_IEEE123_34IEDS+",sep=";")
#                XIED=dirto.iloc[0:np.size(dirto,0),:].values
MMED, IED,MMED1=get_measures(X1,Xd1,XIED,Lin);
t=np.zeros((193))
for k in range(193):
    t[k]=0+0.0005181347*k
for kt in range(1):
    IMM=MN
    IMD=Sd
#################Grafica de la señal de corriente############################
# Crear vector de tiempos
    if kt==0:
       MMED=MMED
    else:
       MMED=MMED1     
    plt.figure()
    plt.plot(t,MMED[:,3],'r-*',label='FA')
    plt.plot(t,MMED[:,4],'g-*',label='FB')
    plt.plot(t,MMED[:,5],'k-*',label='FC')
    plt.ylabel('Current [A]')
    plt.xlabel('time [s]')
    plt.grid(True)
##########################################################
    CAct=round(round(np.size(MMED,0)/StW)-(MPC/StW))
    Mdes=np.ones((CAct-1,12))
    Mdes1=np.zeros((CAct-1,12))
# Abrir el modelo en donde se va a evaluar la información
# filename = 'finalized_model.sav'
# loaded_model = pickle.load(open(filename, 'rb'))
## Función para obtener las medidas
    Dat1=np.zeros((np.size(MMED,0),6))
    res=np.zeros((CAct-1))
    band=0
    file=("Neural_Network_V13_L650_632_%s" %(str(int(IED[kt]))))
    #file=("Decision_Tree_%s" %(str(IED)))
    aext=(".joblib")
    file=file+aext
    result=load(file)
    for kr in range(CAct-1):
        if kr==18:
            fg=1
       # Dat=MMED[StW*(kr):MPC+StW*(kr),:]
        #Mdes[kr,:],Mdes1[kr,:]=getatri(Dat[:,0:3],Dat[:,3:6],int(MPC/2),IMM,IMD)
        
        #### 18 atributos
        
        #Mdes=[604.66,729.6,761.36,25.18,20.27,19.81,123.4,121.6,122.8,0,-2.09,2.12,4.9,6,6.2,-0.81,-3,0.88]#Caso 1
        #Mdes=[517.86,645.64,663.12,29.36,22.98,22.74,123.3,121.8,122.8,0,-2.09,2.11,4.2,5.3,5.4,-0.7,-2.9,0.9]#Caso 2
        #Mdes=[468.92,644.48,458.06,32.47,22.94,33.46,123.4,121.6,123.8,0,-2.08,2.12,3.8,5.3,3.7,-0.22,-2.88,0.7]#Caso 3
        #Mdes=[480.7,489.6,297.84,31.62,30.6,51.71,123.3,122.4,124.1,0,-2.08,2.11,3.9,4,2.4,-0.22,-2.94,0.87]#Caso 4
        #Mdes=[480.09,454.36,272.58,31.56,33.19,56.32,123.1,122.8,123.9,0,-2.09,2.11,3.9,3.7,2.2,-0.22,-2.9,1]#Caso 5
        #Mdes=[432.25,585.6,397.76,35.29,25.48,38.84,123.5,122,124.3,0,-2.08,2.12,3.5,4.8,3.2,-0.08,-2.84,0.63]#Caso 6
        #Mdes=[456.95,572.93,591.36,33.38,25.94,25.67,123.5,121.9,123.2,0,-2.09,2.12,3.7,4.7,4.8,-0.63,-2.86,0.88]#Caso 7
        #Mdes=[544.28,669.35,700.53,28.11,22.13,21.56,123.7,121.7,122.9,0,-2.09,2.12,4.4,5.5,5.7,-0.77,-2.98,0.86]#Caso 8
        #Mdes=[400.32,586.56,703.38,39.09,25.46,21.65,125.1,122.2,123.4,0,-2.09,2.12,3.2,4.8,5.7,-1.37,-3.01,0.75]#Caso 9
        Mdes=[443.16,172.9,123.9,34.19,88.21,123.9,123.1,123.5,123.9,0,-2.09,2.12,3.6,1.4,1,-0.09,-2.91,2.33]#Caso 10
        
        
        #####  15 atributos (sin angulos de corriente)
        
        #Mdes=[604.66,729.6,761.36,25.18,20.27,19.81,123.4,121.6,122.8,0,-2.09,2.12,4.9,6,6.2]#Caso 1
        #Mdes=[517.86,645.64,663.12,29.36,22.98,22.74,123.3,121.8,122.8,0,-2.09,2.11,4.2,5.3,5.4]#Caso 2
        #Mdes=[468.92,644.48,458.06,32.47,22.94,33.46,123.4,121.6,123.8,0,-2.08,2.12,3.8,5.3,3.7]#Caso 3
        #Mdes=[480.7,489.6,297.84,31.62,30.6,51.71,123.3,122.4,124.1,0,-2.08,2.11,3.9,4,2.4]#Caso 4
        #Mdes=[480.09,454.36,272.58,31.56,33.19,56.32,123.1,122.8,123.9,0,-2.09,2.11,3.9,3.7,2.2]#Caso 5
        #Mdes=[432.25,585.6,397.76,35.29,25.48,38.84,123.5,122,124.3,0,-2.08,2.12,3.5,4.8,3.2]#Caso 6
        #Mdes=[456.95,572.93,591.36,33.38,25.94,25.67,123.5,121.9,123.2,0,-2.09,2.12,3.7,4.7,4.8]#Caso 7
        #Mdes=[544.28,669.35,700.53,28.11,22.13,21.56,123.7,121.7,122.9,0,-2.09,2.12,4.4,5.5,5.7]#Caso 8
        #Mdes=[400.32,586.56,703.38,39.09,25.46,21.65,125.1,122.2,123.4,0,-2.09,2.12,3.2,4.8,5.7]#Caso 9
        #Mdes=[443.16,172.9,123.9,34.19,88.21,123.9,123.1,123.5,123.9,0,-2.09,2.12,3.6,1.4,1]#Caso 10
        
        
        
        Mdes=np.array(Mdes)
        vregs = (Mdes - IMM[0:18]) / np.sqrt(IMD[0:18])
        fol=vregs
        #fol=Mdes[kr,0:18]
        Prub=fol.reshape(1,-1)
        res[kr]=result.predict(Prub)

        # if kr==0:
        #    if res[kr]==0:
        #        Dat1[0:256,:]=MMED[0:256,:]
        #    else:
        #        Dat1[0:256,:]=MMED[0:256,:]
        #        Dat1[256:np.size(MMED,0),:]=np.zeros((np.size(MMED,0)-256,6))
        #        break
        # else:
        #    if res[kr]==0 and band==0:
        #        Dat1[MPC+StW*(kr-1):MPC+StW*(kr),:]=MMED[MPC+StW*(kr-1):MPC+StW*(kr),:]
        #    else:
        #        Dat1[MPC+StW*(kr-1):MPC+StW*(kr),:]=MMED[MPC+StW*(kr-1):MPC+StW*(kr),:]
        #        Dat1[MPC+StW*(kr):np.size(MMED,0),:]=np.zeros((np.size(MMED,0)-MPC-StW*(kr),6))
        #        break 
    
##############Grafica de la señal de corriente############################
# Crear vector de tiempos
    plt.figure()
    plt.plot(t,Dat1[:,3],'r-*',label='FA')
    plt.plot(t,Dat1[:,4],'g-*',label='FB')
    plt.plot(t,Dat1[:,5],'k-*',label='FC')
    plt.ylabel('Current [A]')
    plt.xlabel('time [s]')
    plt.grid(True)