# Air Quality Network Sensor - Rooftop version

## Urbanova

Source code and documentation for an air quality sensor package based on the Raspberry Pi Model 3 computer and low-cost retail sensors. Measurements are made every 30 
seconds, converted into a JSON string and are recorded then transferred and store at Amazon Web Services (AWS).

* Environmental measurements
	* Temperature, Pressure and Relative Humidity - TPU sensor (BME280 breakout; Adafruit)
    <https://www.adafruit.com/product/2652>
	* Atmospheric Carbon Dioxide Concentration - CO2 sensor (K-30; CO2Meter.com)
    <https://www.co2meter.com/products/k-30-co2-sensor-module>
	* Particulate Matter (PM) in 16 bins including PM1, PM2.5 and PM10 - Particulate sensor (OPC-N2; Alphasense)
    <http://www.alphasense.com/index.php/products/optical-particle-counter/>

* Supporting hardware
	* Single-board computer (Raspberry Pi 3 - Model B)
    <https://www.adafruit.com/product/3055>
	* GPS and Real-time Clock (Ultimate GPS breakout; Adafruit)
    <https://www.adafruit.com/product/746>


### Documentation

* [Initial setup](doc/install/)

* [Connect to Urbanova Cloud / AWS IoT](doc/setup/AWS_IoT_Connectivity.md)
