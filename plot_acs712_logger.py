from datetime import date
import time
import matplotlib.pyplot as plt
import serial
import RPi.GPIO as GPIO
import os
import sys

from read_m5_class import m5logger
from read_acs712_class import read_acs712

today = date.today()
t=time.localtime()
current_time=time.strftime("_H%H_M%M_S%S",t)
fn="ACS_LOG_"+str(today)+current_time+".csv"
#fn_s12="SSR12_"+str(today)+current_time+".csv"
f=open(fn,'w',encoding="utf-8")
#fs12=open(fn_s12,'w',encoding="utf-8")
start = time.time()

ldata0=[0]*10
ldata=[ldata0]*10
ser1 = serial.Serial("/dev/ttyACM0",19200)
ser2 = serial.Serial("/dev/ttyUSB0",115200)
acs712=read_acs712()
sport=m5logger()

data=[0]*10
data02=[0]*10
data2=[data02]*10

#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(12,GPIO.OUT)

sttime=0   # ssr12 time # switching ssr12
ssr12on=0  # ssr12 switch
while True:
 try:
  ttime=time.time()-start
  if ttime<0.001:
    ttime=0.0
  st=time.strftime("%Y %b %d %H:%M:%S", time.localtime())
  ss=str(time.time()-int(time.time()))
  rttime=round(ttime,2)
  curr=acs712.read(ser1)
  array2=sport.read_logger(ser2)
  ss=st+ss[1:5]+","+str(rttime)+","
  ss12=ss
  ss=ss+str(curr)+","
  for i in range(0,len(array2)-1):
    ss=ss+str(array2[i])+","
  ss=ss+str(array2[len(array2)-1])
 
  #  switching ssr12
  # ssr12 timen interval = 200sec
  sw12=""
  path = './go12.txt'
  is_file = os.path.isfile(path)
  if is_file:
    print('go12.txt was found')
    stime=ttime-sttime
    if stime>200.0:
      print(array2[7])
      if float(array2[7])<0:
        ssr12on=1
      else:
        ssr12on=0
      sttime=ttime
    else:
      if ssr12on==1:
        if stime<=float(sys.argv[1]):
 #         GPIO.output(12,True)
          sw12="on"
        else:
 #         GPIO.output(12,False)
          sw12="off"
      else:
 #       GPIO.output(12,False)
        sw12="off"
  else:
     print('go12.txt was not found -> then the ssr12 is off.')
#     GPIO.output(12,False)
     sw12="off"
     
#  ss=ss+","+sw12
  f.write(ss+"\n")
  #
  
  print(ss)
  data.pop(-1)
  data2.pop(-1)
  data.insert(0,curr)
  data2.insert(0,array2)
#  rez = [[data[j][i] for j in range(len(data))] for i in range(len(data[0]))]
  rez2 = [[data2[j][i] for j in range(len(data2))] for i in range(len(data2[0]))]
  x=range(0, 10, 1)
  plt.figure(100)
  plt.clf()
  plt.ylim(0,5000)
  plt.plot(x,data)
#  lin=[0]*8
#  h1=[]
#  for i in range(0,8):
#   lin[i],=plt.plot(x,rez[i],label="A"+str(i))
#  for i in range(0,7):
#    h1.append(lin[i])
#  plt.legend(handles=h1)
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
#  fs12.close()
  ser1.close()
  ser2.close()
  exit()
