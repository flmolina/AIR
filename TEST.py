#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import ADS1263
import RPi.GPIO as GPIO
import matplotlib.pyplot as plt

REF = 5.08          # Modify according to actual voltage
                    # external AVDD and AVSS(Default), or internal 2.5V

# ADC1 test part
TEST_ADC1       = True
# ADC2 test part
TEST_ADC2       = False
# ADC1 rate test part, For faster speeds use the C program
TEST_ADC1_RATE =False
# RTD test part 
TEST_RTD        = False     

try:
    ADC = ADS1263.ADS1263()
    
    # The faster the rate, the worse the stability
    # and the need to choose a suitable digital filter(REG_MODE1)
    if (ADC.ADS1263_init_ADC1('ADS1263_14400SPS') == -1):
        exit()
    ADC.ADS1263_ConfigADC(7, 0xE)
    ADC.ADS1263_SetMode(0) # 0 is singleChannel, 1 is diffChannel9
    # ADC.ADS1263_DAC_Test(1, 1)      # Open IN6
    # ADC.ADS1263_DAC_Test(0, 1)      # Open IN7
    
    if(TEST_ADC1):       # ADC1 Test
        channelList = [0]  # The channel must be less than 10
        vector=[]
        for i in range(0,int(N)):
            ADC_Value = ADC.ADS1263_GetAll(channelList) # get ADC1 value
            for i in channelList:
                if(ADC_Value[i]>>31 ==1):
                    data=(REF*2 - ADC_Value[i] * REF / 0x80000000)
                    print("ADC1 IN%d = -%lf" %(i, data)) 
                else:
                    data=(ADC_Value[i] * REF / 0x7fffffff)
                    print("ADC1 IN%d = %lf" %(i, data))   # (32bit)
                if float(data)<0:
                    print(float(data))
            vector.append(data)        
            for i in channelList:
                print("\33[2A")
        print(min(vector), max(vector))
        plt.plot(vector)
        plt.show()
        
    elif(TEST_ADC2):
        if (ADC.ADS1263_init_ADC2('ADS1263_ADC2_800SPS') == -1):
            exit()
        vector=[]
        for i in range(0,100):
            ADC_Value = ADC.ADS1263_GetAll_ADC2()   # get ADC2 value
            for i in range(0, 10):
                if i==0:
                    if(ADC_Value[i]>>23 ==1):
                        data=(REF*2 - ADC_Value[i] * REF / 0x800000)
                        print("ADC2 IN%d = -%lf"%(i,data ))
                    else:
                        data=(ADC_Value[i] * REF / 0x7fffff)
                        print("ADC2 IN%d = %lf"%(i,data ))     # 24bit
            print("\33[11A")
            vector.append(data)
        plt.plot(vector)
        plt.show()
            
    elif(TEST_ADC1_RATE):    # rate test
        time_start = time.time()
        ADC_Value = []
        isSingleChannel = True
        if isSingleChannel:
            while(1):
                ADC_Value.append(ADC.ADS1263_GetChannalValue(0))
                if len(ADC_Value) == 5000:
                    time_end = time.time()
                    print(time_start, time_end)
                    print(time_end - time_start)
                    print('frequency = ', 5000 / (time_end - time_start))
                    break
        else:
            while(1):
                ADC_Value.append(ADC.ADS1263_GetChannalValue(0))
                if len(ADC_Value) == 5000:
                    time_end = time.time()
                    print(time_start, time_end)
                    print(time_end - time_start)
                    print('frequency = ', 5000 / (time_end - time_start))
                    break

    elif(TEST_RTD):     # RTD Test
        while(1):
            ADC_Value = ADC.ADS1263_RTD_Test()
            RES = ADC_Value / 2147483647.0 * 2.0 *2000.0       #2000.0 -- 2000R, 2.0 -- 2*i
            print("RES is %lf"%RES)
            TEMP = (RES/100.0 - 1.0) / 0.00385      #0.00385 -- pt100
            print("TEMP is %lf"%TEMP)
            print("\33[3A")
        
    ADC.ADS1263_Exit()

except IOError as e:
    print(e)
   
except KeyboardInterrupt:
    print("ctrl + c:")
    print("Program end")
    ADC.ADS1263_Exit()
    exit()
   
