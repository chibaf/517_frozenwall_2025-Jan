import serial
from read_acs712_class import read_acs712
acs712=read_acs712()
ser = serial.Serial("/dev/ttyACM0",9600)
while True:
  print(acs712.read(ser))