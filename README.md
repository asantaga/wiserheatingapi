# Drayton Wiser Hub API v 1.0.10

This repository contains a simple API which queries the Drayton Wiser Heating sysystem used in the UK.

The API functionality provides the following functionality
- Ability to query all rooms
- Ability to query all thermostats and room stats
- Ability to set temperature of room and TRV thermostats
- Ability to query various data about the system (like heating status)
- Ability to query and set and copy schedules
- Ability to query and set smartplugs (modes and states)

The project is closely associated with the Wiser HomeAssitant component availabe here https://github.com/asantaga/wiserHomeAssistantPlatform

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
wiserhubip=192.168.0.22
```

## 5. Run the sample
To help understand the api simply look at the sample code ```wiserapitest.py``` and the fully commented code. 

## 6. Documentation

Documentation available in [docs](docs) directory and within comments in the code

Additionally @steversig has also created a repository with some nice examples which be of use, see https://github.com/steversig/wiserheatingapi-examples


*Changelog*

1.0.2.1 
* Added ability to turn trvs off and then back on by using setRoomMode
* Fixed bug in setRoomTemperature that wasnt checking the ranges properly

1.0.2.2
* Changed temperature variables to be the real variable, and internally *10 

1.0.3
* Merged [pull7](https://github.com/asantaga/wiserheatingapi/pull/7) : Timeout and other improvements. 
    * Fix for [issue 1](https://github.com/asantaga/wiserheatingapi/issues/1) Error when having zero TRVs
    * Fix for [issue 4](https://github.com/asantaga/wiserheatingapi/issues/4)  Setting boost sometimes errors
* Merged [pull5](https://github.com/asantaga/wiserheatingapi/pull/5) :  Ability to turn hotwater on/off/auto 

1.0.4 
* Merged https://github.com/asantaga/wiserheatingapi/pull/9 : Schedule export/import

1.0.5.2
* Added support for smartplugs, both mode and state

1.0.6
* Added support for network data
1.0.7
* Merged [pull17](https://github.com/asantaga/wiserheatingapi/pull/17), Enhancement to detect invalid JSON from the hub, thanks @TobyLL!  fixed bug in getSmartplug state not working correctly
1.0.8 
* Merged [pull20(https://github.com/asantaga/wiserheatingapi/pull/20 ) Fix for TRVs not keeping off setting
1.0.9
* Ability to get,set and copy schedules for all devices

1.0.10
* Added PR#23: Added setRoomScheduleAvance and other APIs from @stevesig (thank you!)

