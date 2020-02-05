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

# Get wiserkey/hubIp from wiserkeys.params file
# This file is not source controlled as it contains the testers secret etc

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


    print ("Devices")
    print ("--------------------------------")

    for device in wh.getDevices():
        print ("Device : Id {} Name {} Type {} , SignalStrength {}  ".format(device.get("id"),device.get("Name"),device.get("ProductType"),device.get("DisplayedSignalStrength")))

    
    print("--------------------------------")
    print ("Schedule for Room1 {}".format(wh.getRoomSchedule(4)))
    print ("--------------------------------")

    # Query Schedule for Room1
    # Big assumption there is always a room 1 :-)
    #
    with open('./room1schedule.json', 'w') as f:
        room1schedule = wh.getRoomSchedule(1)
        json.dump(room1schedule, f)
        f.close()
        print("File room1schedule.json created ")
    # Load schedule file and set schedule
    print("--------------------------------")
    print("Set room schedule for Room 1")
    with open('./room1schedule.json', 'r') as f:
        data = json.load(f)
        wh.setRoomSchedule(1, data)
        f.close
        print("Schedule for room 4 loaded indirectly from file")

    print("--------------------------------")
    # Load schedule and set direct from file
    print("--------------------------------")
    print("Set room schedule from file")
    print("Skipped")
    # wh.setRoomScheduleFromFile(1, "./room1schedule.json")
    # print("Schedule for room 1 loaded directly from file")
    print("--------------------------------")

    print("Copy room schedule")
    print("Skipped")
    #    wh.copyRoomSchedule(4,3)
    print("--------------------------------")


    #  List all Rooms
  
    findValve=0
    roomName=None

    for room in wh.getRooms():
        smartValves=room.get("SmartValveIds")
        if smartValves is None: 
          print("Room {} has no smartValves")
        else:
          print ("Room {}, setpoint={}C, current temp={}C".format(room.get("Name"),room.get("CurrentSetPoint")/10,room.get("CalculatedTemperature")/10    )    )

    # Find and set smartPlug on off
    if (wh.getSmartPlugs() is not None):
        for smartPlug in wh.getSmartPlugs():
            print("Smartplug ID {} Name {} OutputState {}".format(smartPlug.get("id"),smartPlug.get("Name"),smartPlug.get("OutputState")))
            print("Setting Smartplug to current state")
            #wh.setSmartPlugMode(smartPlug.get("id"),smartPlug.get("OutputState"))
            wh.setSmartPlugMode(15,"Off")


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
