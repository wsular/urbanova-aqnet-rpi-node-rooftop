#!/usr/bin/python

# Script to access data from WSU Urbanova Air Quality Network (aqnet) rooftop sensors.
#
# Code and setup notes are archvied at:
#   <https://github.com/wsular/urbanova-aqnet-rpi-node-rooftop>
#
#   Code assembled by:
#           Von P. Walden, Patrick O'Keeffe and Kristian Gubsch
#           Washington State University
#           Laboratory for Atmospheric Research
#

import time
import pandas as pd

def readGPS():
    # Create DataFrame index.
    measurements = [["GPS","GPS","GPS","GPS"], 
                    ["time","latitude","longitude","altitude"]]
    tuples = list(zip(*measurements)) 
    index = pd.MultiIndex.from_tuples(tuples, names=['instruments', 'measurements'])

    GPSreport = session.next()
    while GPSreport['class'] != ['TPV']:
        continue
    
    gpsConnected = False
    while not(gpsConnected):
        GPSreport = session.next()
        if GPSreport['class'] = 'TPV':
            if hasattr(GPSreport, 'time') & hasattr(GPSreport, 'lat') & hasattr(GPSreport, 'lon') & hasattr(GPSreport, 'alt'):
                gpsConnected = True
                GPSdata = pd.DataFrame([GPSreport.time, 
                                        GPSreport.lat, 
                                        GPSreport.lon, 
                                        GPSreport.alt], index = index, columns=['data'])
                break
    return GPSdata

def readBME():
    # Create DataFrame index.
    measurements = [["BME280","BME280","BME280"], 
                    ["temperature","pressure","relative_humidity"]]
    tuples = list(zip(*measurements)) 
    index = pd.MultiIndex.from_tuples(tuples, names=['instruments', 'measurements'])
    
    BMEdata = pd.DataFrame({'temperature': bme280.read_temperature(), 
                            'pressure': bme280.read_pressure(), 
                            'relative_humidity': bme280.read_humidity()})
    return BMEdata

def readOPC():
    # Create DataFrame index.
    measurements = [["OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2"], 
                    ["bin0","bin1","bin2","bin3","bin4","bin5","bin6","bin7","bin8","bin9","bin10","bin11","bin12","bin13","bin14","bin15","SFR","PM1","PM2.5","PM10","Bin1 MToF","Bin3 MToF","Bin5 MToF","Bin7 MToF","Checksum","SamplingPeriod"]]
    tuples = list(zip(*measurements)) 
    index = pd.MultiIndex.from_tuples(tuples, names=['instruments', 'measurements'])

    while True:
        try:
            hist = alpha.histogram()
        except:
            print('WARNING:opc:Data transfer was incomplete')
        time.sleep(1)
    OPCdata = pd.DataFrame([hist["bin0"],
                            hist["bin1"],
                            hist["bin2"],
                            hist["bin3"],
                            hist["bin4"],
                            hist["bin5"],
                            hist["bin6"],
                            hist["bin7"],
                            hist["bin8"],
                            hist["bin9"],
                            hist["bin10"],
                            hist["bin11"],
                            hist["bin12"],
                            hist["bin13"],
                            hist["bin14"],
                            hist["bin15"],
                            hist["SFR"],
                            hist["PM1"],
                            hist["PM2.5"],
                            hist["PM10"],
                            hist["Bin1 MToF"],
                            hist["Bin3 MToF"],
                            hist["Bin5 MToF"],
                            hist["Bin7 MToF"],
                            hist["Checksum"],
                            hist["SamplingPeriod"]], index = index, columns=['data'])
    return OPCdata

def readK30():
    # Create DataFrame index.
    measurements = [["K30"],
                    ["CO2"]]
    tuples = list(zip(*measurements)) 
    index = pd.MultiIndex.from_tuples(tuples, names=['instruments', 'measurements'])

    #ser.write('\xFE\x44\x00\x08\x02\x9F\x25')
    #time.sleep(.01)
    #resp = ser.read(7)
    #high = ord(resp[3])
    #low  = ord(resp[4])
    #co2  = (high*256) + low
    co2  = 400.    # Dummy data for now.
    K30data = pd.DataFrame(co2, index = index, columns=['data'])
    return K30data

############ Open connections for individual sensors ############
# Initialize the Ultimate GPS Breakout
import gps
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
print('    GPS connected!')

# Initialize the BME280 temperature/pressure/humidity sensor.
from Adafruit_BME280 import *
bme280 = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
print('    BMP280 connected!')

# Initialize the K-30 carbon dioxide sensor.
#import serial
#import time
#ser = serial.Serial('/dev/ttyAMA0')
#print('    K-30 Serial Connected!')
#ser.flushInput()
#time.sleep(1)

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

# Set up nice exit for AlphaSense OPC
import atexit
@atexit.register
def cleanup():
    alpha.off()

# Create a blank pandas DataFrame for Aqnet data.
measurements = [["TimeStamp","BME280","BME280","BME280","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","OPC-N2","GPS","GPS","GPS","GPS","K30"],
                ["time","temperature","pressure","relative_humidity","temperature","pressure","bin0","bin1","bin2","bin3","bin4","bin5","bin6","bin7","bin8","bin9","bin10","bin11","bin12","bin13","bin14","bin15","SFR","PM1","PM2.5","PM10","Bin1 MToF","Bin3 MToF","Bin5 MToF","Bin7 MToF","Checksum","SamplingPeriod","time","latitude","longitude","altitude","CO2"]]
tuples = list(zip(*measurements)) 
index = pd.MultiIndex.from_tuples(tuples, names=['instruments', 'measurements'])

# Read data from sensors at certain time interval.
dataInterval = 30  # seconds
while True:
    try:
        # Acquire Aqnet sensor data.
        BMEdata = read280()
        OPCdata = readOPC()
        GPSdata = readGPS()
        K30data = readK30()

        # Pack sensor data into a single DataFrame.
        measurements = [["TimeStamp"],
                        ["time"]]
        tuples = list(zip(*measurements)) 
        index = pd.MultiIndex.from_tuples(tuples, names=['instruments', 'measurements'])
        timeStamp = pd.DataFrame(GPSdata.time, index = index, columns=['data'])
        data      = pd.concat([timeStamp, BMEdata, OPCdata, GPSdata, K30data])

        # Convert DataFrame to a JSON file.
        data.to_json(data_json, orient='table')

        # Transfer JSON file to Amazon Web Services using IoT framework.
        # TBD...

        time.sleep(dataInterval)
    except (KeyboardInterrupt, SystemExit):
        raise
except:
    print('Exception encountered! Ignoring...')


