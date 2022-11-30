import json  # JSON package

from applnlayer.ApplnMessageTypes import GroceryOrderMessage,MessageTypes  # our custom message in native format


# This is the method we will invoke from our driver program to convert a data structure
# in native format to JSON
def serialize(res):
    # create a JSON representation from the original data structure
    json_buf = {
        "type": res.type.value,
        "veggie": res.veggie,
        "drinks": res.drinks,
        "milk": res.milk,
        "bread": res.bread,
        "meat": res.meat
    }

    # return the underlying jsonified buffer
    return bytes(json.dumps(json_buf),"utf-8")


# deserialize the incoming serialized structure into native data type
def deserialize(buf):
    # get the json representation from the incoming buffer
    json_buf = json.loads(buf)

    # now retrieve the native data structure out of it.
    res = GroceryOrderMessage()
    res.type = MessageTypes(json_buf["type"])
    res.veggie = json_buf["veggie"]
    res.drinks = json_buf["drinks"]
    res.milk = json_buf["milk"]
    res.bread = json_buf["bread"]
    res.meat = json_buf["meat"]

    return res

if __name__ == '__main__':
    a = GroceryOrderMessage()
    a.type = MessageTypes.GROCERY
    a.veggie['cucumber'] = 1
    a.veggie['tomato'] = 2
    a.veggie['potato'] = 3
    a.veggie['carrot'] = 4
    a.veggie['eggplant'] = 5
    a.drinks['cans']['beer'] = 1
    a.drinks['cans']['coke'] = 2
    a.drinks['cans']['coffee'] = 3
    a.drinks['bottle']['sprite'] = 4
    a.drinks['bottle']['apple_juice'] = 5
    a.drinks['bottle']['orange_juice'] = 6

    temp = serialize(a)
    b = deserialize(temp)
    print(b)

