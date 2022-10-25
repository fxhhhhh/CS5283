# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Purpose: Provides the skeleton code for our custom application protocol
#          used by our smart refrigerator to send grocery order and health status
#          messages. This is our Application Layer used in the Computer Networks
#          course Assignments
#

# import the needed packages
import sys    # for syspath and system exception
import json  # JSON package
from enum import Enum  # for enumerated types
import os
from applnlayer.ApplnMessageTypes import MessageTypes
from FlatBuffers1 import CustomAppProto
# add to the python system path so that packages can be found relative to
# this directory
sys.path.insert (0, "../")
from applnlayer.ApplnMessageTypes import GroceryOrderMessage
from transportlayer.CustomTransportProtocol import CustomTransportProtocol as XPortProtoObj
from FlatBuffers1 import grocery_serialize as flat_gro_serialize
from FlatBuffers1 import health_serialize as flat_hea_serialize
from FlatBuffers1 import response_serialize as flat_res_serialize
from JSON import grocery_serialize as json_gro_serialize
from JSON import health_serialize as json_hea_serialize
from JSON import response_serialize as json_res_serialize
############################################
#  Serialization Enumeration Type
############################################
class SerializationType (Enum):
  # One can extend this as needed. For now only these two
  UNKNOWN = -1
  JSON = 1
  FBUFS = 2

############################################
#  Bunch of Application Layer Exceptions
#
# @TODO@ Add more, if these are not enough
############################################
class BadSerializationType (Exception):
  '''Bad Serialization Type'''
  def __init__ (self, arg):
    msg = arg + " is not a known serialization type"
    super ().__init__ (msg)

class BadMessageType (Exception):
  '''Bad Message Type'''
  def __init__ (self):
    msg = "bad or unknown message type"
    super ().__init__ (msg)

############################################
#       Custom Application Protocol class
############################################
class CustomApplnProtocol ():
  '''Custom Application Protocol for the Smart Refrigerator'''

  ###############################
  # constructor
  ###############################
  def __init__ (self, role):
    self.role = role  # indicates if we are client = 2 or server = 1,router = 3
    self.ser_type = SerializationType.UNKNOWN
    self.xport_obj = None # handle to our underlying transport layer object
    self.gro_serialize = json_gro_serialize.serialize
    self.hea_serialize = json_hea_serialize.serialize
    self.res_serialize = json_res_serialize.serialize
    self.gro_deserialize = json_gro_serialize.deserialize
    self.res_deserialize = json_res_serialize.deserialize
    self.hea_deserialize = json_hea_serialize.deserialize
  ###############################
  # configure/initialize
  ###############################
  def initialize (self, config, ip, port):
    ''' Initialize the object '''

    try:
      # Here we initialize any internal variables
      print ("Custom Application Protocol Object: Initialize")
      print ("serialization type = {}".format (config["Application"]["Serialization"]))

      # initialize our variables
      if (config["Application"]["Serialization"] == "json"):
        self.ser_type = SerializationType.JSON
      elif (config["Application"]["Serialization"] == "fbufs"):
        self.ser_type = SerializationType.FBUFS
        self.gro_serialize = flat_gro_serialize.serialize
        self.hea_serialize = flat_hea_serialize.serialize
        self.res_serialize = flat_res_serialize.serialize
        self.gro_deserialize = flat_gro_serialize.deserialize
        self.res_deserialize = flat_res_serialize.deserialize
        self.hea_deserialize = flat_hea_serialize.deserialize
      else:  # Unknown; raise exception
        raise BadSerializationType (config["Application"]["Serialization"])

      # Now obtain our transport object
      # @TODO
      print ("Custom Appln Protocol::initialize - obtain transport object")
      self.xport_obj = XPortProtoObj (self.role)

      # initialize it
      print ("Custom Appln Protocol::initialize - initialize transport object")
      self.xport_obj.initialize (config, ip, port)

    except Exception as e:
      raise e  # just propagate it

  ##################################
  #  send Grocery Order
  ##################################
  # here we need to serialize as transport layere will not do
  def send_grocery_order (self, order):
    try:
      # @TODO@ Implement this
      # Essentially, you will need to take the Grocery Order supplied in native host
      # format and invoke the serialization method (either json or flatbuf)

      # You must first check that the message type is grocery order else raise the
      # BadMessageType exception
      #
      # Note, here we are sending some dummy field just for testing purposes
      # but remove it with the correct payload and length.
      if(order.type != MessageTypes.GROCERY):
        raise BadMessageType()
      afterSerialize = self.gro_serialize(order)


      self.xport_obj.send_appln_msg(afterSerialize, len(afterSerialize))

    except Exception as e:
      raise e

  ##################################
  #  send Health Status
  ##################################
  def send_health_status (self, status):
    try:
      # @TODO@ Implement this
      # Essentially, you will need to take the Health Status supplied in native host
      # format and invoke the serialization method (either json or flatbuf)

      # You must first check that the message type is health status else raise the
      # BadMessageType exception
      #
      # Note, here we are sending some dummy field just for testing purposes
      # but remove it with the correct payload and length.
      if (status.type != MessageTypes.HEALTH):
        raise BadMessageType()
      afterSerialize = self.hea_serialize(status)
      self.xport_obj.send_appln_msg(afterSerialize, len(afterSerialize))
    except Exception as e:
      raise e

  ##################################
  #  send response
  ##################################
  def send_response (self, response):
    try:
      # @TODO@ Implement this
      # Essentially, you will need to take the Health Status supplied in native host
      # format and invoke the serialization method (either json or flatbuf)

      # You must first check that the message type is response else raise the
      # BadMessageType exception
      #
      # Note, here we are sending some dummy field just for testing purposes
      # but remove it with the correct payload and length.
      if response.type != MessageTypes.RESPONSE:
        raise BadMessageType()
      afterSerialize = self.res_serialize(response)
      self.xport_obj.send_appln_msg(afterSerialize, len(afterSerialize))

      # print ("CustomApplnProtocol::send_response")
      # self.xport_obj.send_appln_msg (response.dummy, len (response.dummy))
    except Exception as e:
      raise e

  ##################################
  #  receive request
  ##################################
  def recv_request (self):
    try:
      # @TODO@ Implement this
      # receive the message and return it to caller
      #
      # To that end, we ask our transport object to retrieve
      # application level message
      #
      # Note, that in this assignment, we are not worrying about sending
      # transport segments etc and so what we receive from ZMQ is the complete
      # message.
      print ("CustomApplnProtocol::recv_appln_msg")
      request = self.xport_obj.recv_appln_msg ()
      if self.ser_type == SerializationType.JSON:
        json_buf = json.loads(request)
        if MessageTypes(json_buf["type"]) == MessageTypes.GROCERY:
          afterDeserialize = json_gro_serialize.deserialize(request)
          return afterDeserialize
        if MessageTypes(json_buf["type"]) == MessageTypes.HEALTH:
          afterDeserialize = json_hea_serialize.deserialize(request)
          return afterDeserialize
        if MessageTypes(json_buf["type"]) == MessageTypes.RESPONSE:
          afterDeserialize = json_res_serialize.deserialize(request)
          return afterDeserialize
      if self.ser_type == SerializationType.FBUFS:
        try:
          afterDeserialize = flat_res_serialize.deserialize(request)
          print("Nooooooooot Response")
          return afterDeserialize
        except:
          try:
            afterDeserialize = flat_hea_serialize.deserialize(request)
            print("Nooooooooot health")
            return afterDeserialize
          except:
            afterDeserialize = flat_gro_serialize.deserialize(request)
            print("Nooooooooot gro")
            return afterDeserialize



    except Exception as e:
      raise e

  ##################################
  #  receive response
  ##################################
  def recv_response (self):
    try:
      # @TODO@ Implement this
      # receive the message and return it to caller
      #
      # To that end, we ask our transport object to retrieve
      # application level message
      #
      # Note, that in this assignment, we are not worrying about sending
      # transport segments etc and so what we receive from ZMQ is the complete
      # message.
      print ("CustomApplnProtocol::recv_response")
      request = self.xport_obj.recv_appln_msg ()

      if self.ser_type == SerializationType.JSON:
        json_buf = json.loads(request)
        if MessageTypes(json_buf["type"]) == MessageTypes.GROCERY:
          afterDeserialize = json_gro_serialize.deserialize(request)
          return afterDeserialize
        if MessageTypes(json_buf["type"]) == MessageTypes.HEALTH:
          afterDeserialize = json_hea_serialize.deserialize(request)
          return afterDeserialize
        if MessageTypes(json_buf["type"]) == MessageTypes.RESPONSE:
          afterDeserialize = json_res_serialize.deserialize(request)
          return afterDeserialize
      if self.ser_type == SerializationType.FBUFS:
        try:
          afterDeserialize = flat_res_serialize.deserialize(request)
          print("Nooooooooot Response")
          return afterDeserialize
        except:
          try:
            afterDeserialize = flat_hea_serialize.deserialize(request)
            print("Nooooooooot health")
            return afterDeserialize
          except:
            afterDeserialize = flat_gro_serialize.deserialize(request)
            print("Nooooooooot gro")
            return afterDeserialize
        # tryDe = flat_gro_serialize.deserialize1(request)
        # if tryDe.type == MessageTypes.GROCERY:
        #   afterDeserialize = flat_gro_serialize.deserialize(request)
        #   print(afterDeserialize)
        #   return afterDeserialize
        # if tryDe.type == MessageTypes.HEALTH:
        #   afterDeserialize = flat_hea_serialize.deserialize(request)
        #   return afterDeserialize
        # if tryDe.type == MessageTypes.RESPONSE:
        #   afterDeserialize = flat_res_serialize.deserialize(request)
        #   return afterDeserialize

      # return response
    except Exception as e:
      raise e

