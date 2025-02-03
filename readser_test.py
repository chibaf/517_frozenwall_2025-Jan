import serial
from readser_class import readser
read_ser1=readser()
read_ser2=readser()
ser1 = serial.Serial("/dev/ttyACM0",9600)
ser2 = serial.Serial("/dev/ttyACM1",9600)
while True:
  print(read_ser1.read(ser1))
  print(read_ser2.read(ser2))