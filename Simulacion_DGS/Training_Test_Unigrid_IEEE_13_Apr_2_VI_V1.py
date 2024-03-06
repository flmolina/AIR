# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 09:17:47 2021

@author: juang
"""
## This code allow obtaining the data base for each IED, them the information will use to analyze the effect
## of IED"s location over the accuracy
## the maximum number of scenarios foer each class: 1080

from os import scandir
import numpy as np
import pandas as pd
import random
import math
from sklearn.utils import shuffle
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

#This function helps to read a directory
def ls2(path): #Sirve para listar los archivos de una carpeta
    return [obj.name for obj in scandir(path) if obj.is_file()]


# This function helps to get the measures of current and voltage
def get_measures(X1,Xd1,Xs1):
       Reles1=np.zeros((np.size(X1,0),6))
       Reles2=np.zeros((np.size(X1,0),6))
    #Convertir Lin en Li,LF,No1 y No2
       if Xs1[0]==111 or Xs1[1]==111:
          Li=("LPCC")
          Lf=("-%s" %(str(Xs1[1])))
       else:
          Li=("L%s" %(str(Xs1[0])))
          Lf=("-%s" %(str(Xs1[1])))
       if Xs1[0]==111 or Xs1[1]==111:
          No1="PCC"
          No2=("N%s" %(Xs1[1]))
       else:
          No1=("N%s" %(Xs1[0]))
          No2=("N%s" %(Xs1[1]))
    # Se obtienen los IEDs asociados a la línea
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
               Reles1[kp,0:3]=X1[kp,int(Posten1-2):int(Posten1+1)]
          if Poscor==Poscorx:
             for kp in range(np.size(X1,0)): 
                 Reles1[kp,3:6]=X1[kp,int(Poscor-5):int(Poscor-2)]
          else:
             for kp in range(np.size(X1,0)): 
                 Reles1[kp,3:6]=X1[kp,int(Poscor-2):int(Poscor+1)] 
          for kp in range(np.size(X1,0)):
              Reles2[kp,0:3]=X1[kp,int(Posten2-2):int(Posten2+1)]
          for kp in range(np.size(X1,0)):
              Reles2[kp,3:6]=X1[kp,int(Poscorx-2):int(Poscorx+1)]
       else:
          for kp in range(np.size(X1,0)):
              Reles1[kp,0:3]=X1[kp,int(Posten1-2):int(Posten1+1)]
          Reles1[:,3:6]=np.zeros((np.size(X1,0),3))
          for kp in range(np.size(X1,0)):
              Reles2[kp,0:3]=X1[kp,int(Posten2-2):int(Posten2+1)]
          Reles2[:,3:6]=np.zeros((np.size(X1,0),3)) 
       return Reles1,Reles2

def getatri(V,I,Tsi,Tfal,Tout):
    M=np.size(V,0)
    puntos=round(M/(60*Tsi)); #Puntos o muestras por ciclo
    Cfal=Tfal*60;# ciclo donde se va tomar la información de la falla
    P1=puntos*Cfal;#Numero de puntos de donde comienza la falla
    VI=np.zeros((puntos,6))    
    #Ainv=np.array([[1,1,1],[1,complex(-0.5,0.866025),complex(-0.5,-0.866025)],[1,complex(-0.5,-0.866025),complex(-0.5,0.866025)]])
    VI[:,0:3]=V[int(P1-(puntos/2)+Tout):int(P1+(puntos/2)+Tout),:] # medio ciclo de nofalla y medio de falla para V
    #VI[:,3:6]=V[int(P1+Tout):int(P1+puntos+Tout),:]
    VI[:,3:6]=I[int(P1-(puntos/2)+Tout):int(P1+(puntos/2)+Tout),:] # medio ciclo de nofalla y medio de falla para V
    #VI[:,9:12]=I[int(P1+Tout):int(P1+puntos+Tout),:]
    VIf=np.zeros((puntos,6),dtype=complex)
    for ky in range(6):
        VIfx=np.fft.fft(VI[:,ky])
        VIf[:,ky]=VIfx
    #temp=np.max(np.abs(VIf[0:P/2,6]))
    pos=np.argmax(np.abs(VIf[0:int(puntos/2),3]))
    VIfinal=VIf[pos,:]*2/puntos
    V1=VIfinal[0:3]
    I1=VIfinal[3:6]
    Vmag=np.abs(V1)/math.sqrt(2)
    Imag=np.abs(I1)/math.sqrt(2)
    Vang=np.angle(V1)
    Iang=np.angle(I1)
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
    des[0,0:3]=temp[0,0:3] #Potencia por fase
    des[0,3:6]=temp1[0,0:3] # impedancia porfase
    des[0,6:9]=Vmag[0:3]
    des[0,9:12]=Vang[0:3]
    des[0,12:15]=Imag[0:3]
    des[0,15:18]=Iang[0:3]
   
    des1F=np.zeros((1,18))
    
    #####################################
    
    
    ### Información de Potencia ######
    des1F[0,0:3]=des[0,0:3]*1000000

    #############################################
    
    ###  Información de impedancia #####
    des1F[0,3:6]=des[0,3:6]

    ###################################
    
    ###Información  de magnitudes y angulos voltajes #######
    des1F[0,6:9]=des[0,6:9]*1000
    des1F[0,9:12]=des[0,9:12]
   #################
    
    ###Información  de magnitudes y angulos voltajes y corriente#######
    des1F[0,12:15]=des[0,12:15]*1000
    des1F[0,15:18]=des[0,15:18]
    
    ##################################################
    
    
    return des1F

def Base_data(Info,TIIE,TXs):
    Info1=np.zeros((int(TIIE),np.size(Info,1)))
    Info1[0:int(TIIE),:]=Info[0:int(TIIE),:]
    Info1X=np.zeros((int(TIIE),np.size(Info,1)-1))
    Info1Y=np.zeros((int(TIIE),1))
    #Randomized 
    Info1=shuffle(Info1)
    #Standarized
    scaler=StandardScaler()
    Info1X=scaler.fit_transform(Info1[:,0:18])
    Scamean=scaler.mean_
    Scavar=scaler.var_
    Info1Y=Info1[:,18]
    #Splited
    InfoX_train, InfoX_test, Infoy_train, Infoy_test = train_test_split(Info1X, Info1Y, test_size=0.25,random_state=1,stratify=Info1Y)
    #Save Test data base
    archivo=open(('C:\\Juan_python\IUnigrid_TestV10_App2_18F_%s.csv' %(str(TXs))),'w')
    for k in range(np.size(InfoX_test,0)):
        for G in range(np.size(InfoX_test,1)):
            archivo.write('%5f' %InfoX_test[k][G])
            archivo.write(',')
        archivo.write('%5f' %Infoy_test[k])
        archivo.write('\n')    
    #Save Training data base
    archivo=open(('C:\\Juan_python\IUnigrid_TrainV10_App2_18F_%s.csv' %(str(TXs))),'w')
    for k in range(np.size(InfoX_train,0)):
        for G in range(np.size(InfoX_train,1)):
            archivo.write('%5f' %InfoX_train[k][G])
            archivo.write(',')
        archivo.write('%5f' %Infoy_train[k])
        archivo.write('\n') 
    archivo=open(('C:\\Juan_python\IUnigrid_MeanVar_V10_App2_18F_%s.csv' %(str(TXs))),'w')
    for k in range(np.size(Scamean)):
        archivo.write('%5f' %Scamean[k])
        archivo.write(',')
        archivo.write('%5f' %Scavar[k])
        archivo.write('\n') 
        
#Vector de relación entre IEDs 22-20
#Vaux=[1,2,3,4,5,6,5,7,8,9,8,10,11,12,13,14,15,16,17,18,19,20]
#Vector de muestras ventana
VecW=[-12,-6,-3,0,3,6,12]
VecWFal=[-12,-6,-3,0,3,6,12]
#VecW=[-40,-30,-20,-10,0,10,20,30,40]
#VecWFal=[-40,-30,-20,-10,0,10,20,30,40]
#Scenario information
dirto=pd.read_csv("Escenarios_Falla_Unigrid_falla_V4.csv",sep=",")
Xf_d=dirto.iloc[0:np.size(dirto,0),:].values
dirto=pd.read_csv("Escenarios_Falla_Unigrid_No_falla_V7.csv",sep=",")
Xf_dnf=dirto.iloc[0:np.size(dirto,0),:].values
## Relays information 
dirto=pd.read_csv("Reles_Unigrid.csv",sep=";")
XIED=dirto.iloc[0:np.size(dirto,0),:].values
# #Back-up Matrix
# dirto=pd.read_csv("Matriz_de_respaldos.csv",sep=";")
# Xmr=dirto.iloc[0:np.size(dirto,0),:].values
# TXmr=np.size(Xmr,0)
# # Constraint matrix
# dirto=pd.read_csv("Matriz_Restricciones.csv",sep=";")
# Xres=dirto.iloc[0:np.size(dirto,0),:].values
#Topologia del sistema se determina el número de IEDS
dirto=pd.read_csv("Topologia_Unigrid.csv",sep=";")
Xs=dirto.iloc[0:np.size(dirto,0),:].values
TXs=np.size(Xs,0)#Número de IEDS 
direc=ls2("D:\CSV_digsilent_Falla_Unigrid_V4")
Tar=len(direc)
direcnf=ls2("D:\CSV_digsilent_No_Falla_Unigrid_V7")
Tarnf=len(direcnf)



# Este proceso se debe hacer para cada IED
datos=np.zeros((TXs*2,3000000,19))
TIIE=np.zeros((1,2*TXs))
for ky in range (TXs): #Tópologia
#  if ky>=2:  
    #Información de no falla
    gh=0
    gh1=0
    fg=0
    for k in range(Tarnf):
        direcnf1=direcnf[k]# Main archive
        ASD=("D:\CSV_digsilent_No_Falla_Unigrid_V7//")      
        AS=ASD+direcnf1
        fid=pd.read_csv(AS,header=None,sep=";")
        Xd1=fid.iloc[0,:].values
        X1=fid.iloc[2:194,:].values
        Re1,Re2=get_measures(X1,Xd1,Xs[ky,:])
        for kl in range(Tarnf):
            direcrand=direcnf[kl]# The archive should be random
            AS1=ASD+direcrand
            fid1=pd.read_csv(AS1,header=None,sep=";")
            X1rand=fid1.iloc[2:194,:].values
            Rerd1 ,Rerd2=get_measures(X1,Xd1,Xs[ky,:])
            if Xf_dnf[int(direcnf1[9:int(len(direcnf1)-4)]),3]<7 and Xf_dnf[int(direcrand[9:int(len(direcrand)-4)]),3]<7 or (Xf_dnf[int(direcnf1[9:int(len(direcnf1)-4)]),3]>10 and Xf_dnf[int(direcrand[9:int(len(direcrand)-4)]),3]>10):
               Re1[round(np.size(X1,0)/2):np.size(X1,0),:]=Rerd1[round(np.size(X1,0)/2):np.size(X1,0),:]
               Re2[round(np.size(X1,0)/2):np.size(X1,0),:]=Rerd2[round(np.size(X1,0)/2):np.size(X1,0),:]
               for hj in range(len(VecW)):
                   datos[ky*2][gh,0:18]=getatri(Re1[:,0:3],Re1[:,3:6],0.1,0.05,VecW[hj])
                   datos[ky*2][gh,18]=0
                   gh=gh+1
               for hj in range(len(VecW)):
                   datos[2*ky+1][gh1,0:18]=getatri(Re2[:,0:3],Re2[:,3:6],0.1,0.05,VecW[hj])
                   datos[ky*2+1][gh1,18]=0
                   gh1=gh1+1
            elif Xf_dnf[int(direcrand[9:int(len(direcrand)-4)]),3]==10 or Xf_dnf[int(direcnf1[9:int(len(direcnf1)-4)]),3]==10:
                Re1[round(np.size(X1,0)/2):np.size(X1,0),:]=Rerd1[round(np.size(X1,0)/2):np.size(X1,0),:]
                Re2[round(np.size(X1,0)/2):np.size(X1,0),:]=Rerd2[round(np.size(X1,0)/2):np.size(X1,0),:]
                for hj in range(len(VecW)):
                    datos[ky*2][gh,0:18]=getatri(Re1[:,0:3],Re1[:,3:6],0.1,0.05,VecW[hj])
                    datos[ky*2][gh,18]=1
                    gh=gh+1
                    fg=fg+1
                for hj in range(len(VecW)):
                    datos[2*ky+1][gh1,0:18]=getatri(Re2[:,0:3],Re2[:,3:6],0.1,0.05,VecW[hj])
                    datos[ky*2+1][gh1,18]=1
                    gh1=gh1+1
        #Obtener atributos para cada uno de reles
    #Here we are going to program the code to the fault scenario for prymary and back-up protection
    for k in range(Tar):
        direc1=direc[k]# Main archive
        ASD=("D:\CSV_digsilent_Falla_Unigrid_V4//")
        AS=ASD+direc1
        fid=pd.read_csv(AS,header=None,sep=";")
        Xd1=fid.iloc[0,:].values
        X1=fid.iloc[2:194,:].values
        if Xs[ky,0]==111:
           Xss="PCC"        
           Xss1=str(Xs[ky,1])
        else:
           Xss=str(Xs[ky,0])
           Xss1=str(Xs[ky,1])
        if ky==0:
          if (Xss=="650" and Xss1=="632") or (Xss=="633" and Xss1=="634") or (Xss=="632" and Xss1=="671"):
             Re1 ,Re2=get_measures(X1,Xd1,Xs[ky,:])
             for hj in range(len(VecWFal)):
                datos[ky*2][gh,0:18]=getatri(Re1[:,0:3],Re1[:,3:6],0.1,0.05,VecWFal[hj])
                datos[ky*2][gh,18]=1
                gh=gh+1
             for hj in range(len(VecWFal)):
                datos[2*ky+1][gh1,0:18]=getatri(Re2[:,0:3],Re2[:,3:6],0.1,0.05,VecWFal[hj])
                datos[ky*2+1][gh1,18]=1
                gh1=gh1+1
          else:
             Re1 ,Re2=get_measures(X1,Xd1,Xs[ky,:])
             for hj in range(len(VecWFal)):
                datos[ky*2][gh,0:18]=getatri(Re1[:,0:3],Re1[:,3:6],0.1,0.05,VecWFal[hj])
                datos[ky*2][gh,18]=0
                gh=gh+1
             for hj in range(len(VecWFal)):
                datos[2*ky+1][gh1,0:18]=getatri(Re2[:,0:3],Re2[:,3:6],0.1,0.05,VecWFal[hj])
                datos[ky*2+1][gh1,18]=0
                gh1=gh1+1 
        if ky==1:
          if Xss==Xf_d[int(direc1[9:int(len(direc1)-4)]),4][1:4] and Xss1==Xf_d[int(direc1[9:int(len(direc1)-4)]),4][5:8]:
             Re1 ,Re2=get_measures(X1,Xd1,Xs[ky,:])
             for hj in range(len(VecWFal)):
                datos[ky*2][gh,0:18]=getatri(Re1[:,0:3],Re1[:,3:6],0.1,0.05,VecWFal[hj])
                datos[ky*2][gh,18]=1
                gh=gh+1
             for hj in range(len(VecWFal)):
                datos[2*ky+1][gh1,0:18]=getatri(Re2[:,0:3],Re2[:,3:6],0.1,0.05,VecWFal[hj])
                datos[ky*2+1][gh1,18]=1
                gh1=gh1+1 
          else:
             Re1 ,Re2=get_measures(X1,Xd1,Xs[ky,:])
             for hj in range(len(VecWFal)):
                datos[ky*2][gh,0:18]=getatri(Re1[:,0:3],Re1[:,3:6],0.1,0.05,VecWFal[hj])
                datos[ky*2][gh,18]=0
                gh=gh+1
             for hj in range(len(VecWFal)):
                datos[2*ky+1][gh1,0:18]=getatri(Re2[:,0:3],Re2[:,3:6],0.1,0.05,VecWFal[hj])
                datos[ky*2+1][gh1,18]=0
                gh1=gh1+1  
        if ky==2:
         if (Xss=="632" and Xss1=="671") or (Xss=="632" and Xss1=="680") or (Xss=="692" and Xss1=="675"):
             Re1 ,Re2=get_measures(X1,Xd1,Xs[ky,:])
             for hj in range(len(VecWFal)):
                datos[ky*2][gh,0:18]=getatri(Re1[:,0:3],Re1[:,3:6],0.1,0.05,VecWFal[hj])
                datos[ky*2][gh,18]=1
                gh=gh+1
             for hj in range(len(VecWFal)):
                datos[2*ky+1][gh1,0:18]=getatri(Re2[:,0:3],Re2[:,3:6],0.1,0.05,VecWFal[hj])
                datos[ky*2+1][gh1,18]=1
                gh1=gh1+1 
         else:
             Re1 ,Re2=get_measures(X1,Xd1,Xs[ky,:])
             for hj in range(len(VecWFal)):
                datos[ky*2][gh,0:18]=getatri(Re1[:,0:3],Re1[:,3:6],0.1,0.05,VecWFal[hj])
                datos[ky*2][gh,18]=0
                gh=gh+1
             for hj in range(len(VecWFal)):
                datos[2*ky+1][gh1,0:18]=getatri(Re2[:,0:3],Re2[:,3:6],0.1,0.05,VecWFal[hj])
                datos[ky*2+1][gh1,18]=0
                gh1=gh1+1         
        # Reconocer el IED
    TIIE[0,2*ky]=gh# tamaño de escenarios por cada IED 
    TIIE[0,2*ky+1]=gh1# tamaño de escenarios por cada IED 
    Base_data(datos[2*ky][0:int(TIIE[0,2*ky]),:],TIIE[0,2*ky],int(2*ky))
    #Base_data(datos[2*ky+1][0:int(TIIE[0,2*ky+1]),:],TIIE[0,2*ky+1],int(2*ky+1))
    
#No fault data base

#Hacer una funcion que entregue la base de datos para IED



# Get features

#fault data base
