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

f.close

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
    
    print("--------------------------------")
    print ("Schedule output {}".format(wh.getRoomSchedule(4)))
    print ("--------------------------------")

    # Query Schedule for Room4
    with open('./room4schedule.json', 'w') as f:
        room4schedule = wh.getRoomSchedule(4)
        json.dump(room4schedule, f)
        f.close()
        print("File room4schedule.json created ")
    # Load schedule file and set schedule
    print("--------------------------------")
    print("Set room schedule")
    with open('./room4schedule.json', 'r') as f:
        data = json.load(f)
        wh.setRoomSchedule(4, data)
        f.close
        print("Schedule for room 4 loaded indirectly from file")

    print("--------------------------------")
    # Load schedule and set direct from file
    print("--------------------------------")
    print("Set room schedule from file")
    wh.setRoomScheduleFromFile(4, "./room4schedule.json")
    print("Schedule for room 4 loaded directly from file")
    print("--------------------------------")

#    print("--------------------------------")
#    print("Copy room schedule")
#    wh.copyRoomSchedule(4,3)
#    print("--------------------------------")


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
