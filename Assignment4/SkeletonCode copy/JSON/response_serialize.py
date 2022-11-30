#  Author: Aniruddha Gokhale
#  Created: Fall 2022
#  (based on code developed for Distributed Systems course in Fall 2019)
#
#  Purpose: demonstrate serialization of user-defined packet structure
#  using JSON
#
#  Here our packet or message format comprises a sequence number, a timestamp,
#  and a data buffer of several uint32 numbers (whose value is not relevant to us)

import json # JSON package

from applnlayer.ApplnMessageTypes import ResponseMessage,MessageTypes,contents_type,code_type # our custom message in native format

# This is the method we will invoke from our driver program to convert a data structure
# in native format to JSON
def serialize (res):

  # create a JSON representation from the original data structure
  json_buf = {
    "type" : res.type.value,
    "code" : res.code.value,
    "contents":res.contents.value,
  }
  
  # return the underlying jsonified buffer
  return bytes(json.dumps(json_buf), "utf-8")

# deserialize the incoming serialized structure into native data type
def deserialize (buf):

  # get the json representation from the incoming buffer
  json_buf = json.loads(buf)

  # now retrieve the native data structure out of it.
  res = ResponseMessage ()
  res.type = MessageTypes(json_buf["type"])
  res.code = code_type(json_buf["code"])
  res.contents = contents_type(json_buf["contents"])

  return res
    
    
