from wiserHeatingAPI import wiserHub
import logging
import json

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

# Get Wiser Parameters from keyfile
with open('wiserkeys.params', 'r') as f:
            data = f.read().split('\n')
wiserkey=""
wiserip=""

for lines in data:
   line=lines.split('=')
   if line[0]=='wiserkey':
      wiserkey=line[1]
   if line[0]=='wiserhubip':
      wiserip=line[1]

print (' Wiser Hub IP= {} , WiserKey= {}'.format(wiserip,wiserkey))



#####

try:
#
    wh = wiserHub.wiserHub(wiserip,wiserkey)
    
    # wh.refreshdata()
    # print("itrv 8 is in room {}".format(wh.getDeviceRoom(8)['roomName']))
    # Heating State
    print ("Hot water status {} ".format(wh.getHeatingRelayStatus()))
    print ("Roomstat humidity {}".format(wh.getRoomStatData(1).get("MeasuredHumidity")))
    print (" Room Data {} ".format(wh.getRooms()))
    print("--------------------------------")
    print (" Room 1 data {} ")
  
    print("--------------------------------")
    print("--------------------------------")
    dev=wh.getDevices()
    print (" Device Data {} ".format(dev))
    print ("--------------------------------")
    print (" Device 1 data {} ".format(wh.getDevice(1).get("id")))
#  First get Rooms
  
    findValve=0
    roomName=None
    for room in wh.getRooms():
        smartValves=room.get("SmartValveIds")
        for id in smartValves:
            if (id==findValve):
                roomName=room.get("Name")
                break
        if roomName!=None:
            break
# For devices in room.SmartValveIds:
    print ("Found Valve in room {}".format(roomName))
# Setting HOME Mode , change to AWAY for away mode
    wh.setHomeAwayMode("HOME")
#    wh.setHomeAwayMode("AWAY",200)
    
except json.decoder.JSONDecodeError as ex:
    print("JSON Exception")
