#!/usr/bin/python3

from datetime import date
import time
import matplotlib.pyplot as plt
import serial
import RPi.GPIO as GPIO
import os
import sys

from read_m5_class import m5logger
from readser_class import readser

today = date.today()
t=time.localtime()
current_time=time.strftime("_H%H_M%M_S%S",t)
fn="ACS_LOG_"+str(today)+current_time+".csv"
f=open(fn,'w',encoding="utf-8")
start = time.time()

ldata0=[0]*10
ldata=[ldata0]*10
ser1 = serial.Serial("/dev/ttyACM0",9600)
ser2 = serial.Serial("/dev/ttyUSB0",115200)
read_ser=readser()
sport=m5logger()

data=[0]*10
data02=[0]*10
data2=[data02]*10

while True:
 try:
  ttime=time.time()-start
  if ttime<0.001:
    ttime=0.0
  st=time.strftime("%Y %b %d %H:%M:%S", time.localtime())
  ss=str(time.time()-int(time.time()))
  rttime=round(ttime,2)
  curr=read_ser.read(ser1)
  print(curr)
  cur=0.0
  print(curr[0])
  if curr[0]=="CUR":
    cur=curr[1]
  print(cur)
  array2=sport.read_logger(ser2)
  ss=st+ss[1:5]+","+str(rttime)+","
  ss12=ss
  ss=ss+str(cur)+","
  for i in range(0,len(array2)-1):
    ss=ss+str(array2[i])+","
  ss=ss+str(array2[len(array2)-1])
  f.write(ss+"\n")
  
  print(ss)
  data.pop(-1)
  data2.pop(-1)
  data.insert(0,float(cur))
  data2.insert(0,array2)
  rez2 = [[data2[j][i] for j in range(len(data2))] for i in range(len(data2[0]))] # transposing a matrix
  x=range(0, 10, 1)
  plt.figure(100)
  plt.clf()
  plt.ylim(0,400000)
  plt.plot(x,data)
  plt.pause(0.1)
  plt.figure(200)
  plt.clf()
  plt.ylim(-25,30)
  tl=[0]*10
  h2=[]
  for i in range(0,10):
   tl[i],=plt.plot(x,rez2[i],label="T"+str(i))
  for i in range(0,10):
    h2.append(tl[i])
  plt.legend(handles=h2)
  plt.pause(0.1)
 except KeyboardInterrupt:
  f.close()
  ser1.close()
  ser2.close()
  exit()
