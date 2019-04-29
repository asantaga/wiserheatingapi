# Drayton Wiser Hub API v 1.0.0

This repository contains a simple API which queries the Drayton Wiser Heating sysystem used in the UK.

The API functionality provides the following functionality
- Ability to query all rooms
- Ability to query all thermostats and room stats
- Ability to set temperature of room and TRV thermostats
- Ability to query various data about the system (like heating status)

## Installation



## 1. Find your HeatHub Secret key
Reference https://it.knightnet.org.uk/kb/nr-qa/drayton-wiser-heating-control/#controlling-the-system
1. Press the setup button on your HeatHub, the light will start flashing
Look for the Wi-Fi network (SSID) called **‘WiserHeatXXX’** where XXX is random
2. Connect to the network from a Windows/Linux/Mac machine
3. Execute the secret url :-)
   * For Windows use `Invoke-RestMethod -Method Get -UseBasicParsing -Uri http://192.168.8.1/secret/` 
   * For Linux (or Windows WSL) use `curl http://192.168.8.1/secret`

   This will return a string which is your system secret, store this somewhere. If you are running the test script simply put this value , with the ip address of the hub, in your wiserkeys.params

4. Press the setup button on the HeatHub again and it will go back to normal operations
5. Copy the secret and save it somewhere.
## 3. Find Your HEATHUB IP

Using your router, or something else, identify the IP address of your HeatHub, it usually identifies itself as the same ID as the ``WiserHeatXXXXXX`` 

## 4. Add values in you wiserkeys.params
Create a file called wiserkeys.params and place two lines, one with the wiser IP and the other with the key it self. 
e.g.
```
wiserkey=ABCDCDCDCCCDCDC
wiserip=192.168.0.22
```

## 5. Run the sample
To help understand the api simply look at the sample code ```wiserapitest.py```
