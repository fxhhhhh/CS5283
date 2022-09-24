# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
#
# Purpose: Provides the definition of supported messages
#

# import the needed packages
import sys
from enum import Enum  # for enumerated types

from typing import List

# @TODO import whatever more packages are needed

# add to the python system path so that packages can be found relative to
# this directory
sys.path.insert(0, "../")


class milk_type(Enum):
    one = 1
    two = 2
    free = 3
    whole = 4
    almond = 5
    cashew = 6
    oat = 0


class meat_type(Enum):
    pork = 1
    lamp = 2
    beef = 0

class dispenser_type(Enum):
    PTIMAL = 0
    PARTIAL = 1
    BLOCKAGE = 2

class status_type(Enum):
    Good = 0
    Bad = 1

class code_type(Enum):
    Ok = 0
    BAD_REQUEST = 1

class contents_type(Enum):
    Order_Placed = 0
    You_are_Healthy = 1
    Bad_Request = 2

class bread_type(Enum):
    whole_wheat = 1
    pumpernicke = 2
    rye = 0

############################################
#  Enumeration for Message Types
############################################
class MessageTypes(Enum):
    # One can extend this as needed. For now only these two
    UNKNOWN = -1
    GROCERY = 0
    HEALTH = 1
    RESPONSE = 2


############################################
#  Grocery Order Message
############################################
class GroceryOrderMessage:
    '''Grocery Order Message'''

    def __init__(self):
        self.dummy = "This is a grocery order message"

        # @TODO - the above is simply to test the code. You need to get rid of that dummy
        # and replace it with the complex data struture we have for the grocery order
        # as represented in the host (as a Python language data structure)
        self.type = MessageTypes.GROCERY
        self.veggie = {
            'cucumber': 0,
            'tomato': 0,
            'potato': 0,
            'carrot': 0,
            'eggplant': 0,
        }
        self.drinks = {
            'cans': {
                'beer': 0,
                'coke': 0,
                'coffee': 0,
            },
            'bottle': {
                'sprite': 0,
                'apple_juice': 0,
                'orange_juice': 0,
            }
        }

        self.milk = []


        self.bread = []


        self.meat = []

    def __str__(self):
        '''Pretty print the contents of the message'''
        print("print the content of Grocery Order Message")
        # @TODO - remove the above print stmt and instead create a pretty print logic
        print("Type: {}".format(self.type))
        print("Veggie: {}".format(self.veggie))
        print("Drinks: {}".format(self.drinks))
        print("Milk: {}".format(self.milk))
        print("Bread: {}".format(self.bread))
        print("Meat: {}".format(self.meat))
        return "1"


############################################
#  Health Status Message
############################################
class HealthStatusMessage:
    '''Health Status Message'''

    def __init__(self):

        # @TODO - the above is simply to test the code. You need to get rid of that dummy
        # and replace it with the complex data struture we have for the health status
        # as represented in the host (as a Python language data structure)

        self.type = MessageTypes.HEALTH
        self.dispenser = dispenser_type.PTIMAL

        self.icemaker = 0
        self.lightbulb = 0
        self.fridge_temp = 0
        self.freezer_temp = 0


        self.sensor_status = status_type

    def __str__(self):
        '''Pretty print the contents of the message'''

        # @TODO - remove the above print stmt and instead create a pretty print logic
        print("Dispenser: {}".format(self.dispenser))
        print("Icemaker: {}".format(self.icemaker))
        print("Lightbulb: {}".format(self.lightbulb))
        print("Fridge_temp: {}".format(self.fridge_temp))
        print("Sensor_status: {}".format(self.sensor_status))
        return "1"


############################################
#  Response Message
############################################
class ResponseMessage:
    '''Response Message'''

    def __init__(self):
        # @TODO - the above is simply to test the code. You need to get rid of that dummy
        # and replace it with the data struture we have for the response message
        # as represented in the host (as a Python language data structure)
        self.type = MessageTypes.RESPONSE
        self.code = code_type.Ok

        self.contents = contents_type.You_are_Healthy

    def __str__(self):
        '''Pretty print the contents of the message'''

        # @TODO - remove the above print stmt and instead create a pretty print logic
        print("Code: {}".format(self.code))
        print("Contents: {}".format(self.contents))
        return "1"



