import time
from Adafruit_BME280 import *

bme280 = BME280(t_mode=BME280_OSAMPLE_8, p_mode=BME280_OSAMPLE_8, h_mode=BME280_OSAMPLE_8)
print('    BMP280 connected!')

while True:
    print('BME280 Temperature (C)  ', bme280.read_temperature())
    print('BME280 Pressure    (kPa)', bme280.read_pressure()/100.)
    print('BME280 RH          (%)  ', bme280.read_humidity())
    time.sleep(1)

