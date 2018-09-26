#!/usr/bin/python

# Script to access data from WSU Urbanova Aqnet Rooftop sensors.
#
# <https://github.com/wsular/urbanova-aqnet-rpi-node-rooftop.git>

# Initialize the Ultimate GPS Breakout
import gps
session = gps.gps("localhost", "2947")
session.stream(gps.WATCH_ENABLE | gps.WATCH_NEWSTYLE)
print('    GPS connected!')

while True:
    try:
        GPSreport = session.next()
        if GPSreport['class'] == 'TPV':
            if hasattr(GPSreport, 'time'):
                print('GPS    time     ', GPSreport.time)
            if hasattr(GPSreport, 'lat'):
                print('GPS    latitude ', GPSreport.lat)
            if hasattr(GPSreport, 'lon'):
                print('GPS    longitude', GPSreport.lon)
            if hasattr(GPSreport, 'alt'):
                print('GPS    altitude  ',GPSreport.alt)
    except KeyboardInterrupt, SystemExit:
        raise
    except:
        print('Exception encountered! Ignoring...')

