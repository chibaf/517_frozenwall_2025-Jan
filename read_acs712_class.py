class read_acs712:

  def read(self,ser):
    import serial
    line = ser.readline()
    try:
      data=line.strip().decode('utf-8')
    except UnicodeDecodeError:
      return 0
    return data