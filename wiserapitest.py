from wiserHeatingAPI import wiserHub
import logging
import json
import time

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.DEBUG)

# Get Wiser Parameters from keyfile
with open('wiserkeys.params', 'r') as f:
            data = f.read().split('\n')
wiserkey = ""
wiserip = ""

# Get wiserkey/hubIp from wiserkeys.params file
# This file is not source controlled as it contains the testers secret etc

for lines in data:
    line = lines.split('=')
    if line[0] == 'wiserkey':
        wiserkey = line[1]
    if line[0] == 'wiserhubip':
        wiserip = line[1]

print(' Wiser Hub IP= {} , WiserKey= {}'.format(wiserip, wiserkey))


try:
    wh = wiserHub.wiserHub(wiserip, wiserkey)

    print("-------------------------------")
    print("Running tests")
    print("-------------------------------")

    # Display some states
    # Heating State
    print("Hot water status {} ".format(wh.getHotwaterRelayStatus()))
    # Assumes at least one roomstat
    print("Roomstat humidity {}".format(wh.getRoomStatData(1).
                                        get("MeasuredHumidity")))

    print("--------------------------------")
    print("List of Devices")
    print("--------------------------------")

    for device in wh.getDevices():
        print("Device : Id {} Name {} Type {} , SignalStrength {}  ".
              format(device.get("id"),
                     device.get("Name"),
                     device.get("ProductType"),
                     device.get("DisplayedSignalStrength")
                     )
              )
    #
    #Assume there room 1 :-), otherwise what are you heating?
    #
    scheduleRoomTest=1
    print("--------------------------------")
    print("Schedule for Room1 {}".format(wh.getRoomSchedule(scheduleRoomTest)))
    print("--------------------------------")

    # Query Schedule for Room1
    # Big assumption there is always a room 1 :-)
    #
    with open('./room1schedule.json', 'w') as f:
        room1schedule = wh.getRoomSchedule(scheduleRoomTest)
        json.dump(room1schedule, f)
        f.close()
        print("File room1schedule.json created ")
    # Load schedule file and set schedule
    print("--------------------------------")
    print("Set room schedule for Room {}".format(scheduleRoomTest))
    with open('./room1schedule.json', 'r') as f:
        data = json.load(f)
        wh.setRoomSchedule(scheduleRoomTest, data)

        print("Schedule for room {} loaded indirectly from file".format(scheduleRoomTest))

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
  
    findValve = 0
    roomName = None

    print("--------------------------------")
    print("Listing all Rooms")
    print("--------------------------------")
    for scheduleRoomTest in wh.getRooms():
        smartValves = scheduleRoomTest.get("SmartValveIds")
        if smartValves is None: 
          print("Room {} has no smartValves")
        else:
          print("Room {}, setpoint={}C, current temp={}C".
                format(scheduleRoomTest.get("Name"),
                       scheduleRoomTest.get("CurrentSetPoint") / 10,
                       scheduleRoomTest.get("CalculatedTemperature") / 10
                       )
                )

    print("--------------------------------")
    print ("Listing all smartplugs")
    print("--------------------------------")

    # Find and set smartPlug on off
    if wh.getSmartPlugs() is not None:
        for smartPlug in wh.getSmartPlugs():
            smartPlugId=smartPlug.get("id")
            print("Smartplug ID {} Name {} OutputState is {} Mode is {}".
                  format(smartPlug.get("id"),
                         smartPlug.get("Name"),
                         wh.getSmartPlugState(smartPlugId),
                         wh.getSmartPlugMode(smartPlugId)
                  ))
            print("Bouncing Plug {} ".format(smartPlugId))
            originalPlugState=wh.getSmartPlugState(smartPlugId)
            if originalPlugState == "On":
                wh.setSmartPlugState(smartPlug.get("id"), "Off")
                time.sleep(1)
            else:
                wh.setSmartPlugState(smartPlug.get("id"), "On")
                time.sleep(1)
            #Set back to original state
            wh.setSmartPlugState(smartPlugId, originalPlugState)



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
