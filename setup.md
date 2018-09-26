## Air Quality Network Rooftop Units



### Components

* Single-board computer (Raspberry Pi 3 - Model B)
    <https://www.adafruit.com/product/3055>
* GPS and Real-time Clock (Ultimate GPS breakout; Adafruit)
    <https://www.adafruit.com/product/746>
* TPU sensor (BME280 breakout; Adafruit)
    <https://www.adafruit.com/product/2652>
* CO2 sensor (K-30; CO2Meter.com)
    <https://www.co2meter.com/products/k-30-co2-sensor-module>
* Particulate sensor (OPC-N2; Alphasense)
    <http://www.alphasense.com/index.php/products/optical-particle-counter/>

### Assembly

Connect all the sensors directly to the Pi. Do not use a separate power supply
for the OPC-N2 (in contradiction to the software repo readme).

> Through trial-and-error, it is determined that the OPC-N2 exhibits a high
> sensitivity to input voltage and grounding differentials between its data
> and power lines. To avoid the dreaded "your firmware could not be detected"
> error, ensure that both power input and power ground lines are completely
> tied to the Pi Zero's 5V and G rails, respectively. 
>
> In practice, the Pi can source 1.5A through it's 5V GPIO pins. You are
> therefore advised to power the OPC-N2 through the Pi. 


### Initial Setup

1. Purchase a 128-GB Sandisk Ultra microSDXC UHS-1 memory card (with adapter).

2. Download the last version of the Jessie operating system for the Raspberry Pi computer at:
       http://downloads.raspberrypi.org/raspbian/images/raspbian-2017-07-05/2017-07-05-raspbian-jessie.zip

3. Install the Jessie operating system on the memory card using the instructions at:
       https://www.raspberrypi.org/documentation/installation/installing-images/README.md

   Note that these instructions depend on what type of computer you are using (Windows, Mac, Linux).

4. With `raspi-config`:
    1. Change the password. Used the lab password and appended X, where X is the rooftop unit number.
    2. Set approp locale/kb/tz
    3. ~~Set the hostname to `airqualityX`~~, where X is the rooftop unit number. 
            Will set later using Pi's serial number
    4. Enable SPI
    5. Enable I2C
    6. Disable shell on serial port, but keep the serial port hardware enabled.
    7. Enable SSH server
    8. Disable wait for network at boot
    9. Choose to "Update" in raspi-config
5. Reboot
6. `sudo apt-get dist-upgrade`
7. Install basic utilities:
    `sudo apt-get install tux`
    `sudo apt-get install htop`
    `sudo apt-get install build-essential`  (Might already be up-to-date.)
    `sudo apt-get install python-dev`


8. Set up the Ulimate GPS breakout:
    From https://learn.adafruit.com/adafruit-ultimate-gps-on-the-raspberry-pi/setting-everything-up
        `sudo apt-get install gpsd gpsd-clients python-gps`
        `sudo systemctl stop gpsd.socket`
        `sudo systemctl disable gpsd.socket`
        `sudo gpsd /dev/ttyUSB0 -F /var/run/gpsd.sock`

    To test:
        `cgps -s`    (GPS must have acquired lock on satellites.)

9. Enable NPT stats: edit `/etc/ntp.conf` to uncomment line starting
    with `statsdir /var/log/ntpstats/`

10. Setup watchdog service
    1. install watchdog timer using `sudo apt-get install watchdog`
    2. edit `/boot/config.txt` to contain `dtoverlay=watchdog=on`
       [ref](https://github.com/raspberrypi/linux/issues/1285#issuecomment-182264729)
    3. fixup the systemd service file [thanks to](https://kd8twg.net/2015/10/30/raspberry-pi-enabling-watchdog-on-raspbian-jessie/):
       edit `/lib/systemd/system/watchdog.service` to contain:

        ```
        [Install]
        WantedBy=multi-user.target
        ```

    4. edit `/etc/watchdog.conf` to contain
       [ref](https://blog.kmp.or.at/watchdog-for-raspberry-pi/)

        ```
        watchdog-device = /dev/watchdog
        watchdog-timeout = 10
        interval = 2
        max-load-1 = 24
        ```

    5. enable service and start it using sytemctl
        `sudo systemctl enable watchdog`
        `sudo systemctl start watchdog`
        
    6. finally, test it with a fork bomb: `:(){ :|:& };:`
       the Pi should return a PID number, then hang, then reboot

11. Enable persistent system logs: `sudo mkdir -p /var/log/journal`
    [ref](https://www.digitalocean.com/community/tutorials/how-to-use-journalctl-to-view-and-manipulate-systemd-logs)

12. Download supporting packages for various sensors
    1. install `python-pip`
    2. `pip install spidev`
    3. `mkdir aqnet/software/`   (Patrick, note that this directory could be renamed to something more appropriate.)
    4. `cd aqnet/software`
    3. `git clone https://github.com/raspberrypi/weather-station`
    4. `git clone https://github.com/dhhagan/py-opc.git`
    5. `git clone https://github.com/adafruit/Adafruit_Python_GPIO`
    6. `git clone https://github.com/adafruit/Adafruit_Python_BME280`
    7. `cd Adafruit_Python_GPIO && sudo python setup.py install`
    8. `cd ..`
    9. `cd Adafruit_Python_BME280 && sudo python setup.py install`
   10. `cd ..`
   11. `cd py-opc && sudo python setup.py install`

!!! This is where Von's work stopped on Tuesday, 21 August 2018 !!!
!!! But the steps above should be all that are necessary to get all of the rooftop sensors setup for operation !!!


------------- SKIP INTERNET SETUP FOR NOW -------------------------------------
5. [Enable Ethernet Gadget mode](https://learn.adafruit.com/turning-your-raspberry-pi-zero-into-a-usb-gadget?view=all)
    1. edit `/boot/config.txt` to contain `dtoverlay=dwc2`
    2. edit `/boot/cmdline.txt` to contain `modules-load=dwc2,g_ether`
       directly after `rootwait`
6. Set static IP on device -- add to `/etc/network/interfaces`

    > This step superceded by `install.sh`.

    ```
    allow-hotplug usb0
    iface usb0 inet static
        address 10.20.0.2
        netmask 255.255.255.0
        network 10.20.0.0
        broadcast 10.20.0.255
        gateway 10.20.0.1 # upstream computer
    ```

> To share internet from upstream Debian-ish computer, first connect
> Pi0 and identify it's interface (typ `usb0`). Also identify the upstream
> interface with internet access (prob. `wlan0` or `eth0` on your computer).
> 
> 1. Setup a static IP address for the interface created by Pi0:
> 
>     ```
>     allow-hotplug usb0
>     iface usb0 inet static
>         address 10.11.12.1
>         netmask 255.255.255.0
>         network 10.11.12.0
>         broadcast 10.11.12.255
>     ```
>
> 2. Install `dnsmasq` and use this for `/etc/dnsmasq.conf` (for DNS
>    resolution on Pi0 side):
>
>     ```
>     interface=usb0
>     listen-address=10.11.12.1
>     bind-interfaces
>     server=8.8.8.8 # or whatever
>     domain-needed
>     bogus-priv
>     dhcp-range=10.11.12.2,10.11.12.100,1h
>     ```
> 
> 3. Create iptables rules (assuming Pi0 is `usb0` and internet comes
>    from `eth0`) (**NB results not saved after reboot**): 
>    `sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE`
>    if additional firewall rules were present, probably also need:
>
>    ```
>    sudo iptables -A FORWARD -i usb0 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT
>    sudo iptables -A FORWARD -i eth0 -o usb0 -j ACCEPT
>    ```
>
> 4. *also need to enable packet forwarding?*:
>    edit `/etc/sysctl.conf` to enable `net.ipv4.ip_forward=1`
>    and to set immediately:
>    `sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward`
>
> ref: <http://raspberrypi.stackexchange.com/a/50073>

7. If you are working on a different Pi, power off and put the SD card
   into the sensor's Pi0 now. The sensory hardware, clock, etc should
   all be assembled
8. Login to Pi0 via ssh from an upstream linux computer with internet
   access.
-------------------------------------------------------------------------------

> Setting up shared internet connection:
>
> On gateway computer:
>
> 1. Must have static IP 10.11.12.1 (Pi0 expects this address as the DNS server)
> 2. Enable packet forwarding:
>    `sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward`
> 3. Configure bridge between `wlp2s1` (source, typ. `wlan0`) and `enx1e6f988025b1`
>    (the random interface created by Pi0 on gateway)
>
> ```
> sudo iptables -t nat -A POSTROUTING -o wlp2s1 -j MASQUERADE
> #sudo iptables -A FORWARD -i wlp2s1 -o enx1e6f988025b1 -m state --state RELATED,ESTABLISHED -j ACCEPT
> #sudo iptables -A FORWARD -i enx1e6f988025b1 -o wlan0 -j ACCEPT
> ```
>
> ... Only really need the masquerade line.



#### For demonstration purposes

* Prevent console screen from going blank (b/c there is no way to wake it up)
    * http://superuser.com/a/154388/301363
    * http://raspberrypi.stackexchange.com/a/3714/54372
    * http://unix.stackexchange.com/q/8056/160424
    * https://www.raspberrypi.org/forums/viewtopic.php?f=108&t=133519
* Enable auto login to console
* print messages to terminal associated with HDMI display
  (`/dev/tty1`) instead of script's stdout
* force HDMI output so display occurs even if HDMI cord missing at boot time
  (edit `/boot/config.txt` as approp)
* auto-start at boot using `~/.bashrc`; press ^C after login to
  exit prototype script

> autostart options that don't work well:
>
> * cron @reboot (maybe worth retrying)
> * .bashrc (starts for every shell session)
> * /etc/rc.local (no errors, no output)
> * systemd service (can uncapture stdout but requires restart after
>   boot to see output; oddly, can see output in boot messages but
>   not once login presented?)

### Requirements

| Name              | Required by
|-------------------|---------------------------
| `git`             | *
| `pip`             | *
| `python-smbus`    | DS3231,
| `i2c-tools`       | DS3231,
| `build-essential` | BMP280,
| `python-dev`      | BMP280,
| `python-smbus`    | BMP280,
| `python-serial`   | K30,



### Software TODO

* replace manual log file creation with `logging` or `logbook`
    * even better, store data into database instead of flat files
* use non-blocking timing mechanism
    * replace `sleep` with recursively launched function
    * a threaded helper for each sensor?
* properness
    * ~~turn off OPC-N2 at script exit~~


----

## RPi-Monitor Integration

For small projects, [RPi-Monitor](https://github.com/XavierBerger/RPi-Monitor)
is a good quick-and-dirty solution that achieves:

* local system monitoring (cpu, disk space, uptime, etc)
* round-robin database storage (rrdtool)
* web interface (no SSH req'd for monitoring)
* plotting (with time zoom)

The documentation is not spectacular, but it's easy to get started
(copied from the debian packaage install docs):

```
sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 2C0D3C0F
sudo wget http://goo.gl/vewCLL -O /etc/apt/sources.list.d/rpimonitor.list
sudo apt-get update
sudo apt-get install rpimonitor
```

Open a web browser and navigate to `http://10.11.12.13:8888`. There should 
be a warning about "Update needed...". Pull updates and enable automatic 
updates to keep current:

```
sudo /etc/init.d/rpimonitor update
sudo /etc/init.d/rpimonitor install_auto_package_status_update
```

Now copy the relevant modified template files into the appropriate folder.

> Hasn't been integrated into the install script yet.

```
sudo cp etc/rpimonitor/* /etc/rpimonitor/
```
