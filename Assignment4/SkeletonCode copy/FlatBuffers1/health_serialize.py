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


from applnlayer.ApplnMessageTypes import HealthStatusMessage,dispenser_type,MessageTypes
import FlatBuffers1.CustomAppProto.Health.Health as msg
import FlatBuffers1.CustomAppProto.Grocery.messagetypes as msgType


def serialize(hm):
    builder = flatbuffers.Builder(0);

    # let us create the serialized msg by adding contents to it.
    # Our custom msg consists 5 parts
    msg.Start(builder)  # serialization starts with the "Start" method
    msg.AddType(builder, msgType.messagetypes.HEALTH)
    msg.AddIcemaker(builder,hm.icemaker)
    msg.AddLightbulb(builder,hm.lightbulb)
    msg.AddFridgeTemp(builder,hm.fridge_temp)
    msg.AddFreezerTemp(builder,hm.freezer_temp)
    msg.AddDispenser(builder,hm.dispenser.value)
    serialized_msg = msg.End(builder)  # get the topic of all these fields

    # end the serialization process
    builder.Finish(serialized_msg)

    # get the serialized buffer
    buf = builder.Output()

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
    hm = HealthStatusMessage()

    packet = msg.Health.GetRootAs(buf, 0)
    hm.type = MessageTypes(packet.Type())
    hm.fridge_temp = packet.FridgeTemp()
    hm.freezer_temp = packet.FreezerTemp()
    hm.icemaker = packet.Icemaker()
    hm.lightbulb = packet.Lightbulb()
    hm.dispenser = dispenser_type(packet.Dispenser())
    return hm


# deserialize from frames
def deserialize_from_frames(recvd_seq):
    """ This is invoked on list of frames by zmq """

    # For this sample code, since we send only one frame, hopefully what
    # comes out is also a single frame. If not some additional complexity will
    # need to be added.
    assert (len(recvd_seq) == 1)
    # print ("type of each elem of received seq is {}".format (type (recvd_seq[i])))
    print("received data over the wire = {}".format(recvd_seq[0]))
    hm = deserialize(recvd_seq[0])  # hand it to our deserialize method
    # assuming only one frame in the received sequence, we just send this deserialized
    # custom message
    return hm


if __name__ == '__main__':
    a = HealthStatusMessage()
    a.lightbulb = 1
    a.freezer_temp = 1
    a.icemaker = 1
    a.fridge_temp = 1
    a.dispenser= dispenser_type.PTIMAL
    temp = serialize(a)
    b = deserialize(temp)


