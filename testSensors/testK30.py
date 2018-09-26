# Initialize the K-30 carbon dioxide sensor.
import serial
import time
ser = serial.Serial('/dev/ttyAMA0')
print('    K-30 Serial Connected!')
ser.flushInput()
time.sleep(1)

while True:
    resp = ser.read(7)
    high = ord(resp[3])
    low  = ord(resp[4])
    co2  = (high*256) + low
    ser.write('\xFE\x44\x00\x08\x02\x9F\x25')
    time.sleep(.01)
    print('K30 carbon dioxide (ppmv)', co2)
    time.sleep(1)
    