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


try:
#
    
    wh = wiserHub.wiserHub(wiserip,wiserkey)
    # wh.refreshdata()
    # print("itrv 8 is in room {}".format(wh.getDeviceRoom(8)['roomName']))
    # Heating State
    print ("Hot water status {} ".format(wh.getHotwaterRelayStatus()))
    print ("Roomstat humidity {}".format(wh.getRoomStatData(1).get("MeasuredHumidity")))

    print("--------------------------------")
    print ("Raw Room Data {} ".format(wh.getRooms()))
    print("--------------------------------")

    print("--------------------------------")
    dev=wh.getDevices()
    print (" Device Data {} ".format(dev))
    print ("--------------------------------")

#  List all Rooms
  
    findValve=0
    roomName=None

    for room in wh.getRooms():
        smartValves=room.get("SmartValveIds")
        if smartValves is None: 
          print("Room {} has no smartValves")
        else:
          print ("Room {}, setpoint={}C, current temp={}C".format(room.get("Name"),room.get("CurrentSetPoint")/10,room.get("CalculatedTemperature")/10    )    )


# Other Examples
# Setting HOME Mode , change to AWAY for away mode
#    wh.setHomeAwayMode("HOME")
#    wh.setHomeAwayMode("AWAY",10)
# Set room 4 TRVs to off, which is -200
#    print( wh.getRoom(4).get("Name"))
#    wh.setRoomMode(4,"off")
# Set room 4 TRVs to manual, setting normal scheduled temp
#    wh.setRoomMode(4,"manual")
# Set temperature of room 4 to 13C
#    wh.setRoomTemperature(4,10)
# Set TRV off in room 4 to Off
#    wh.setRoomTemperature(4,-20)

except json.decoder.JSONDecodeError as ex:
    print("JSON Exception")
