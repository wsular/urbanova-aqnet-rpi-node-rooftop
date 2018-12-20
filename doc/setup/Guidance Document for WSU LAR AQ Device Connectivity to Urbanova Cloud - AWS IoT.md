# Guidance Document for WSU LAR AQ Device Connectivity to Urbanova Cloud / AWS IoT

Jon Thompson  
July 3, 2018  
(Adapted to Markdown by Von P. Walden (WSU) on 20 Dec 2018)

## IoT Device Configuration and Registration

Because the Urbanova Cloud user interface console is still in design and develop phase, we will use the native AWS console and workflow (WSU account) to provision IoT services for WSU LAR.

The first step is to <span style="color:green">Onboard a Device</span>:

1.	From the AWS Console (WSU Account) select IoT Core
2.	Choose <span style="color:green">Onboard</span> from the left panel menu
3.	Choose <span style="color:green">Configuring a Device</span>
4.	Select Next to start the configuration workflow
5.	Choose the device local environment settings and select next:
![](ConnectingToAWS.png)
6. Provide a name for your device and select Next
7. Download the <span style="color:green">Connection Kit</span>

&nbsp;&nbsp;&nbsp;&nbsp;The following resources are created when you download the Connection Kit:
	
*	A thing in the AWS Device Registry
*	A policy record to send and receive messages

&nbsp;&nbsp;&nbsp;&nbsp;The Connection Kit includes the following artifacts:

*	A certificate and public private key pair
*	A script to download a root certificate from Semantic and to download the AWS IoT Device SDK if not installed, and a test application to send and receive messages

## Device Local Configuration and IoT Connectivity

1.	Install <span style="color:green">Prerequisites</span>:
 
 &nbsp;&nbsp;&nbsp;&nbsp;The device must have the following perquisites install prior to executing the install script from AWS:
 
 *	**Python** (assuming that Python was selected for SDK)
 *	**Git**
 
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Use the Advanced Package Tool to install the latest version of Git:
 
 ```
 df -h								# Validate Disk Space
 
 sudo apt-get update				# Update latest package information
 
 sudo apt-get dist-upgrade			# Upgrade Package Installed Dependencies
 
 sudo apt-get install git			# Install git
 
 sudo apt-get clean					# Remove APT Archive Package Files
 ```
  
 * **Internet access on port 8883** - The standard port for using MQTT of SSL is port 8883.

2.	Copy the Connection Kit from local computer to your device (command below is just an example of using SCP from unix-based computer):
 
 ```
 scp ~/Downloads/connect_device_package.zip pi@xxx.xxx.xxx:~/urbanova/iot
 ```
  
3.	Unzip the <span style="color:green">Connection Kit</span> on the device
 
 ```
 ssh pi@xxx.xxx.xxx
 
 cd ~/urbanova/iot
 
 unzip connect_device_package.zip
```

4. Add execution permissions
 
 ```
 chmod +x start.sh
 ```

5. Run the start script
 
 ```
 sudo ./start.sh
 ```
 
 The script will download and install a Root Certificate from Semantic and the AWS IoT SDK if not already installed, and start the test application.  The test application increments a counter and sends the counter value to AWS IoT Core once per second.

## IoT Device Connectivity Testing

The <span style="color:green">start.sh</span> executes the example application located at <span style="color:green">aws-iot-device-sdk-python/samples/basicPubSub/basicPubSub.py</span> uses the default messages topic “<span style="color:green">sdk/test/Python</span>” to send messages from the device.

The example application is a good starting point to develop your IoT endpoint messaging architecture.  It is worth taking a look at the source code for this file.  The source code is only 125 lines.

We will now test that messages from the device can be securely subscribed and received from Urbanova Cloud / AWS IoT:

1.	From <span style="color:green">IoT Core</span> select <span style="color:green">Test<span> from the left menu panel
2.	Select Subscribe to a <span style="color:green">Topic</span>
3.	In the Subscription topic text box enter “<span style="color:green">sdk/test/Python</span>”
4.	Click Subscribe and view results below (make sure endpoint application is running)
![](SubscriptionToAWS.png)
