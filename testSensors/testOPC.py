import time

# Initialize the OPC-N2 particle monitor.
import spidev
import opc
spi = spidev.SpiDev()
spi.open(0,0)
spi.mode = 1
spi.max_speed_hz = 500000
opcConnected = False
while not(opcConnected):
    print('Attempting to connect to OPC...')
    time.sleep(1)
    try:
        alpha = opc.OPCN2(spi)
        opcConnected = True
    except:
        continue
print('    OPC-N2 connected!')
# Turn sensor on.
alpha.on()

while True:
    try:
        hist = alpha.histogram()
        print('OPC-N2  PM1   (ug/m^3)', hist['PM1'])
        print('        PM2.5 (ug/m^3)', hist['PM2.5'])
        print('        PM10  (ug/m^3)', hist['PM10'])
    except:
        print('WARNING:opc:Data transfer was incomplete')
    time.sleep(1)
