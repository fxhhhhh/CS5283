#  Author: Aniruddha Gokhale
#  Created: Fall 2021
#  (based on code developed for Distributed Systems course in Fall 2019)
#  Modified: Fall 2022 (changed packet name to not confuse with pub/sub Messages)
#
#  Purpose: demonstrate serialization of user-defined packet structure
#  using flatbuffers
#
#  Here our packet or message format comprises a sequence number, a timestamp,
#  and a data buffer of several uint32 numbers (whose value is not relevant to us)

import os
import sys

# this is needed to tell python where to find the flatbuffers package
# make sure to change this path to where you have compiled and installed
# flatbuffers.  If the python package is installed in your system wide files
# or virtualenv, then this may not be needed
sys.path.append(os.path.join(os.path.dirname(__file__), '/home/gokhale/Apps/flatbuffers/python'))
import flatbuffers  # this is the flatbuffers package we import

from applnlayer.ApplnMessageTypes import GroceryOrderMessage, meat_type, milk_type, bread_type,MessageTypes,HealthStatusMessage
import FlatBuffers1.CustomAppProto.Grocery.Grocery as msg
import FlatBuffers1.CustomAppProto.Health.Health as msg1
import FlatBuffers1.CustomAppProto.Grocery.veggie1 as veg
import FlatBuffers1.CustomAppProto.Grocery.drinks1 as drk
import FlatBuffers1.CustomAppProto.Grocery.cans as cas
import FlatBuffers1.CustomAppProto.Grocery.bottles as bot
import FlatBuffers1.CustomAppProto.Grocery.milk1 as mk
import FlatBuffers1.CustomAppProto.Grocery.messagetypes as msgType

def serialize(gm):
    builder = flatbuffers.Builder(0)



    #get the milk vector
    msg.StartMilkVector(builder,len(gm.milk))
    for item in reversed (gm.milk):
        print("add the milk order{}".format(item))
        mk.Createmilk1(builder,milk_type(item[0]).value,item[1])
        print(milk_type(item[0]).value)
    mkVec = builder.EndVector()

    #bread
    msg.StartBreadVector(builder, len(gm.bread))
    for item in reversed(gm.bread):
        print("add the bread order{}".format(item))
        print(bread_type(item[0]).value)
        print(item[1])
        mk.Createmilk1(builder, bread_type(item[0]).value, item[1])
    bdVec = builder.EndVector()

    #meat
    msg.StartBreadVector(builder, len(gm.meat))
    for item in reversed(gm.meat):
        print("add the meat order{}".format(item))
        mk.Createmilk1(builder, meat_type(item[0]).value, item[1])
    mtVec = builder.EndVector()



    # satrt
    msg.GroceryStart(builder)
    msg.AddType(builder, msgType.messagetypes.GROCERY)

    veggies = veg.Createveggie1(builder,
                                gm.veggie['cucumber'],
                                gm.veggie['tomato'],
                                gm.veggie['potato'],
                                gm.veggie['carrot'],
                                gm.veggie['eggplant'])
    msg.AddVeggie(builder, veggies)

    drinks1 = drk.Createdrinks1(builder, gm.drinks['cans']['beer'],
                         gm.drinks['cans']['coke'],
                         gm.drinks['cans']['coffee'],
                         gm.drinks['bottle']['sprite'],
                         gm.drinks['bottle']['apple_juice'],
                         gm.drinks['bottle']['orange_juice']
                         )


    msg.AddDrinks(builder,drinks1)
    msg.AddMilk(builder,mkVec)
    msg.AddBread(builder,bdVec)
    msg.AddMeat(builder,mtVec)
    serialized_msg = msg.GroceryEnd(builder)



    builder.Finish(serialized_msg)
    buf = builder.Output()
    # get the serialized buffer

    # return this serialized buffer to the caller
    return buf


# serialize the custom message to iterable frame objects needed by zmq
def serialize_to_frames(cm):
    """ serialize into an interable format """
    # We had to do it this way because the send_serialized method of zmq under the hood
    # relies on send_multipart, which needs a list or sequence of frames. The easiest way
    # to get an iterable out of the serialized buffer is to enclose it inside []
    print("serialize custom message to iterable list")
    return [serialize(cm)]


# deserialize the incoming serialized structure into native data type
def deserialize(buf):
    print("start deserialize the grocery order message ")
    gm = GroceryOrderMessage()
    packet = msg.Grocery.GetRootAs(buf, 0)
    gm.type = MessageTypes(packet.Type())

    veggie1 = packet.Veggie()
    temp = dict()
    temp['cucumber'] = veggie1.Cucumber()
    temp['tomato'] = veggie1.Tomato()
    temp['potato'] = veggie1.Potato()
    temp['carrot'] = veggie1.Carrot()
    temp['eggplant'] = veggie1.Eggplant()
    gm.veggie =temp

    drink1 = packet.Drinks()
    can1 = cas.cans()
    bottle1 = bot.bottles()
    can = drink1.Can(can1)
    bottle = drink1.Bottle(bottle1)

    gm.drinks['cans']['beer'] = can.Beer()
    gm.drinks['cans']['coke'] = can.Coke()
    gm.drinks['cans']['coffee'] = can.Coffee()
    gm.drinks['bottle']['sprite'] = bottle.Sprite()
    gm.drinks['bottle']['apple_juice'] = bottle.AppleJuice()
    gm.drinks['bottle']['orange_juice'] = bottle.OrangeJuice()
    milk1 = []
    for i in range(packet.MilkLength()):
        milkTemp = packet.Milk(i)
        milk1.append((milk_type(milkTemp.Type()),milkTemp.Quality()))

    gm.milk = milk1


    bread1 = []
    for i in range(packet.BreadLength()):
        breadTemp = packet.Bread(i)
        bread1.append((bread_type(breadTemp.Type()),breadTemp.Quality()))
    gm.bread = bread1

    meat1 = []
    for i in range(packet.MeatLength()):
        meatTemp = packet.Meat(i)
        meat1.append((meat_type(meatTemp.Type(),meatTemp.Quality())))
    gm.meat = meat1



    return gm





if __name__ == '__main__':
    a = GroceryOrderMessage()
    a.type = MessageTypes.GROCERY
    a.veggie['cucumber'] = 1
    a.drinks['cans']['beer'] = 1
    a.drinks['cans']['coke'] = 1
    a.drinks['cans']['coffee'] = 1
    a.drinks['bottle']['sprite'] = 1
    a.drinks['bottle']['apple_juice'] = 1
    a.drinks['bottle']['orange_juice'] = 1
    correct = serialize(a)
    print(correct)
    #
    #
    # temp = b'\x10\x00\x00\x00\x00\x00\n\x00\x08\x00\x00\x00\x06\x00\x04\x00\n\x00\x00\x00\x02\x00\x01\x00'
    # print(bytearray(temp))
    #
    #
    b = deserialize(correct)
    print(correct)
    #
    # print(b.veggie)
    # print(b.milk)
    # print(b.drinks)
