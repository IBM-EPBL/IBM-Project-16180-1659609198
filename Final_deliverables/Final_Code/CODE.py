import ibmiotf.application
import ibmiotf.device
import time
import random
import sys

# watson device details

organization = "no0d4e"
devicType = "Ultrasonic-sensor"
deviceId = "kt"
authMethod = "token"
authToken = "12345678"

#generate random values for randomo variables (temperature&humidity)



def myCommandCallback(cmd):
    global a
    print("command recieved:%s" %cmd.data['command'])
    control=cmd.data['command']
    print(control)

try:
  deviceOptions={"org": organization, "type": devicType,"id": deviceId,"auth-method":authMethod,"auth-token":authToken}
  deviceCli = ibmiotf.device.Client(deviceOptions)
except Exception as e:
  print("caught exception connecting device %s" %str(e))
  sys.exit()

#connect and send a datapoint "temp" with value integer value into the cloud as a type of event for every 10 seconds
deviceCli.connect()

while True:
    current_bin_level = random.randint(10,70)
    current_bin_weight = random.randint(5,15)

    data_to_publish= {
      'CURRENT_BIN_LEVEL': current_bin_level,
      'CURRENT_BIN_WEIGHT':current_bin_weight
    }


    def myOnPublishCallback():
      print ("DATA PUBLISHED TO IBM WATSON")

    success = deviceCli.publishEvent("Ultrasonic_sensor", "json", data_to_publish, qos=0, on_publish=myOnPublishCallback)

    if not success:
        print("not connected to ibmiot")
    time.sleep(30)

    deviceCli.commandCallback=myCommandCallback
#disconnect the device
deviceCli.disconnect()
