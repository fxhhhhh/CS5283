import json  # JSON package

from applnlayer.ApplnMessageTypes import HealthStatusMessage,MessageTypes,dispenser_type,status_type # our custom message in native format


# This is the method we will invoke from our driver program to convert a data structure
# in native format to JSON
def serialize(res):
    # create a JSON representation from the original data structure
    json_buf = {
        "type": res.type.value,
        "dispenser": res.dispenser.value,
        "icemaker": res.icemaker,
        "Lightbulb": res.lightbulb,
        "Fridge_temp": res.fridge_temp,
        "freezer_temp": res.freezer_temp,
        "Sensor_status": res.sensor_status.value
    }

    # return the underlying jsonified buffer
    return bytes(json.dumps(json_buf), "utf-8")


# deserialize the incoming serialized structure into native data type
def deserialize(buf):
    # get the json representation from the incoming buffer
    json_buf = json.loads(buf)

    # now retrieve the native data structure out of it.
    res = HealthStatusMessage()
    res.type = MessageTypes(json_buf["type"])
    res.dispenser = dispenser_type(json_buf["dispenser"])
    res.icemaker = json_buf["icemaker"]
    res.lightbulb = json_buf["Lightbulb"]
    res.fridge_temp = json_buf["Fridge_temp"]
    res.freezer_temp = json_buf["freezer_temp"]
    res.sensor_status = status_type(json_buf["Sensor_status"])

    return res

if __name__ == '__main__':
    a = HealthStatusMessage()
    a.lightbulb = 1
    a.freezer_temp = 1
    a.icemaker = 1
    a.fridge_temp = 1
    a.dispenser= dispenser_type.PTIMAL
    a.sensor_status = status_type.Good
    temp = serialize(a)
    b = deserialize(temp)
