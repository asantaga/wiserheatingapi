"""
# Wiser API Facade

Angelosantagata@gmail.com


https://github.com/asantaga/wiserheatingapi


This API Facade allows you to communicate with your wiserhub. This API is used by the homeassistant integration available at  https://github.com/asantaga/wiserHomeAssistantPlatform
"""

import logging
import requests

_LOGGER = logging.getLogger(__name__)

"""
Wiser Data URLS
"""
WISERHUBURL = "http://{}/data/domain/"    # SSSS
WISERMODEURL= "http://{}/data/domain/System/RequestOverride"
WISERSETROOMTEMP= "http://{}//data/domain/Room/{}"
WISERROOM="http://{}//data/domain/Room/{}"


class wiserHub():
   

    def __init__(self,hubIP,secret):
        _LOGGER.info("WiserHub API Init")
        self.wiserHubData=None
        self.hubIP=hubIP
        self.hubSecret=secret
        self.headers = {'SECRET': self.hubSecret,'Content-Type': 'application/json;charset=UTF-8'}
        self.device2roomMap={}      # Dict holding Valve2Room mapping convinience variable
        self.refreshData()          # Issue first refresh in init
        
    def refreshData(self):
        """
        Forces a refresh of data
        return: JSON Data
        """
        smartValves=[]
        _LOGGER.info("Updating Wiser Hub Data")
        self.wiserHubData = requests.get(WISERHUBURL.format(
            self.hubIP), headers=self.headers).json()
        _LOGGER.debug("Wiser Hub Data received {} ".format(self.wiserHubData))
        if self.getRooms()!=None:
            for room in self.getRooms():
                roomStatId=room.get("RoomStatId")
                if roomStatId!=None:
                    #RoomStat found add it to the list
                    self.device2roomMap[roomStatId]={"roomId":room.get("id"), "roomName":room.get("Name")}
                smartValves=room.get("SmartValveIds")
                if smartValves!=None:
                    for valveId in smartValves:
                            self.device2roomMap[valveId]={"roomId":room.get("id"), "roomName":room.get("Name")}
                else:
                    _LOGGER.warning(" Room doesnt contain any smart valves, maybe an error/corruption?? ")
            _LOGGER.debug(" valve2roomMap{} ".format(self.device2roomMap))
        else:
            _LOGGER.warning("Wiser found no rooms")
        return self.wiserHubData

        

    def getHubData(self):
        """
        Retrieves the full JSON payload , for functions where I havent provided a API yet

        returns : JSON Data
        """
        if (self.wiserHubData==None):
            self.refreshData()
        return self.wiserHubData

    def getRooms(self):
        """
        Gets Room Data as JSON Payload
        """
        if (self.wiserHubData==None):
            self.refreshData()
        return self.wiserHubData.get("Room")
    def getRoom(self,roomId):
        """
        Convinience to get data on a single room

        param roomId: The roomID
        return:
        """
        if (self.wiserHubData==None):
            self.refreshData()
        if (self.wiserHubData.get("Room")==None):
            _LOGGER.warning("getRoom called but no rooms found")
            return None
        for room in (self.wiserHubData.get("Room")):
            if (room.get("id")==roomId):
                return room
        return None

    def getSystem(self):
        """
        Convinience function to get system information

        return: JSON with system data
        """
        if (self.wiserHubData==None):
            self.refreshData()
        return self.wiserHubData.get("System")

    def getHotwater(self):
        """
        Convinience function to get hotwater data

        return: JSON with hotwater data

        """
        if (self.wiserHubData==None):
            self.refreshData()
        return self.wiserHubData.get("HotWater")

    def getHeatingChannels(self):
        """
        Convinience function to get heating channel data

        return: JSON data
        """
        if (self.wiserHubData==None):
            self.refreshData()
        return self.wiserHubData.get("HeatingChannel")

    def getDevices(self):
        """
        Convinience function to get devices data

        return: JSON data
        """
        if (self.wiserHubData==None):
            self.refreshData()
        return self.wiserHubData.get("Device")

    def getDevice(self,deviceId):
        """
        Get single devices data

        param deviceId:
        return: Device JSON Data
        """
        if (self.wiserHubData==None):
            self.refreshData()
        if (self.wiserHubData.get("Device")==None):
            _LOGGER.warning("getRoom called but no rooms found")
            return None
        for device in (self.wiserHubData.get("Device")):
            if (device.get("id")==deviceId):
                return device
        return None


    def getDeviceRoom(self,deviceId):
        """
        Convinience function to return the name of a room which is associated with a device (roomstat or trf)

        param deviceId:
        return: Name of Room associated with a device ID

        """
        _LOGGER.debug(" getDeviceRoom called, valve2roomMap is {} ".format(self.device2roomMap))
        if not self.device2roomMap:
            self.refreshData()
        return self.device2roomMap[deviceId]

    def getHeatingRelayStatus(self):
        """
        Returns heating relay status
        return:  On or Off
        """
        if (self.wiserHubData==None):
            self.refreshData()
        heatingRelayStatus="Off"
        # There could be multiple heating channels, 
        heatingChannels=self.getHeatingChannels()
        for heatingChannel in heatingChannels:
            if heatingChannel.get("HeatingRelayState")=="On":
                heatingRelayStatus="On"
        return heatingRelayStatus
    
    def getHotwaterRelayStatus(self):
        """
         Returns hotwater relay status
        return:  On or Off

        """

        if (self.wiserHubData==None):
            self.refreshData()
        return self.wiserHubData.get("HotWater")[0].get("WaterHeatingState")
    
    def getRoomStatData(self,deviceId):
        """
        Gets Roomt Thermostats Data

        param deviceId:
        return:
        """
        if (self.wiserHubData==None):
            self.refreshData()
        if (self.wiserHubData['RoomStat']==None):
                _LOGGER.warning("getRoom called but no rooms found")
                return None
        for roomStat in self.wiserHubData['RoomStat']:
            if roomStat.get("id")==deviceId:
                return roomStat
        return None 

    def setHomeAwayMode(self,mode,temperature=10):
        """
        Sets default Home or Away mode, optionally allows you to set a temperature for away mode

        param mode: HOME   | AWAY

        param temperature: Temperature between 5-30C or -20 for OFF

        return:
        """
        _LOGGER.info("Setting Home/Away mode to : {} {} C".format(mode,temperature))
        self.response=""
        self.patchData={}
        if (mode not in ['HOME','AWAY']):
            raise Exception("setAwayHome can only be HOME or AWAY")

        if (mode=="AWAY"):
            if temperature==None:
                raise Exception("setAwayHome set to AWAY but not temperature set")
            if temperature== -20 or temperature <0 or temperature>30:
              raise Exception("setAwayHome temperature can only be between 5 and 30 or -20(Off)")
        _LOGGER.info("Setting Home/Away : {}".format(mode))
        temperature=temperature*10
        if (mode=="AWAY"):
            self.patchData={"type":2,"setPoint":temperature}
        else:
            self.patchData={"type":0,"setPoint":0}
        _LOGGER.debug ("patchdata {} ".format(self.patchData))
        self.response = requests.patch(url=WISERMODEURL.format(self.hubIP), headers=self.headers,json =self.patchData )
        if (self.response.status_code!=200):
            _LOGGER.debug("Set Home/Away Response code = {}".format(self.response.status_code))
            raise Exception("Error setting Home/Away , error {} {}".format(self.response.status_code, self.response.text))



    def setRoomTemperature(self, roomId, temperature):
        """
        Sets the room temperature
        param roomId:  The Room ID
        param temperature:  The temperature in celcius from 5 to 30, -20 for Off
        """
        _LOGGER.info("Set Room {} Temperature to = {} ".format(roomId,temperature))
        if ((temperature!=-20) and (temperature<5 or temperature>30)):
            raise Exception("SetRoomTemperature : value of temperature must be between 5 and 30 OR -20 (off)")
        apitemp=temperature*10
        patchData={"RequestOverride":{"Type":"Manual","SetPoint":apitemp}}
        self.response = requests.patch(WISERSETROOMTEMP.format(
            self.hubIP,roomId), headers=self.headers,json=patchData)
        
        if self.response.status_code != 200:
            _LOGGER.error("Set Room {} Temperature to = {} resulted in {}".format(roomId,temperature,self.response.status_code))
            raise Exception("Error setting temperature, error {} ".format(self.response.text))
        _LOGGER.debug("Set room Temp, error {} ({})".format(self.response.status_code, self.response.text))




    # Set Room Mode (Manual, Boost,Off or Auto )
    # If set to off then the trv goes to manual and temperature of -200
    #
    def setRoomMode(self,roomId, mode,boost_temp=20,boost_temp_time=30):
        """
        Set the Room Mode, this can be Auto, Manual, off or Boost. When you set the mode back to Auto it will automatically take the scheduled temperature

        param roomId: RoomId

        param mode:  Mode (auto, manual off, or boost)

        param boost_temp:  If boosting enter the temperature here in C, can be between 5-30

        param boost_temp_time:  How long to boost for in minutes

        """
        # TODO
        _LOGGER.debug("Set Mode {} for a room {} ".format(mode,roomId))
        if (mode.lower()=="auto"):
            #Do Auto
            patchData= {"Mode":"Auto"}
        elif (mode.lower()=="boost"):
            temp=boost_temp*10
            _LOGGER.debug("Setting Boost Temp to {}".format(temp))
            patchData={"RequestOverride":{"Type":"Manual","DurationMinutes": boost_temp_time, "SetPoint":temp, "Originator":"App"}}
        elif (mode.lower()=="manual"):
            # When setting back to manual , set the temp to the scheduled temp
            newTemp=self.getRoom(roomId).get("ScheduledSetPoint")
            patchData = {"Mode": "Manual",
                         "RequestOverride": {"Type": "Manual",
                                             "SetPoint": newTemp}}


        # Implement trv off as per https://github.com/asantaga/wiserheatingapi/issues/3
        elif (mode.lower()=="off"):
            patchData = {"Mode": "Manual","RequestOverride": {"Type": "Manual","SetPoint": -200}}
        else:
            raise Exception("Error setting setting room mode, received  {} but should be auto,boost,off or manual ".format(mode))
        
        # if not a boost operation cancel any current boost
        if (mode.lower()!="boost"):
            cancelBoostPostData={"RequestOverride":{"Type":"None","DurationMinutes": 0, "SetPoint":0, "Originator":"App"}}
            
            self.response = requests.patch(WISERROOM.format(self.hubIP,roomId), headers=self.headers,json=cancelBoostPostData)
            if (self.response.status_code != 200):
                _LOGGER.error("Cancelling boost resulted in {}".format(self.response.status_code))
                raise Exception("Error cancelling boost {} ".format(mode))

        # Set new mode
        self.response = requests.patch(WISERROOM.format(
            self.hubIP,roomId), headers=self.headers,json=patchData)        
        if self.response.status_code != 200:
            _LOGGER.error("Set Room mode to {} resulted in {}".format(mode,self.response.status_code))
            raise Exception("Error setting mode to error {} ".format(mode))
        

    
    

