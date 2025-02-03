import serial
from readser_class import readser
read_ser1=readser()
read_ser2=readser()
ser1 = serial.Serial("/dev/ttyACM0",19200)
ser2 = serial.Serial("/dev/ttyACM1",19200)
while True:
  print(read_ser1.read(ser1))
  print(read_ser2.read(ser2))