# import the needed packages

import os  # for OS functions
import sys  # for syspath and system exception
import time  # for sleep
import argparse  # for argument parsing
import configparser  # for configuration parsing
import zmq  # actually not needed here but we are printing zmq version and hence needed

# add to the python system path so that the following packages can be found
# relative to this directory
sys.path.insert(0, os.getcwd())

from networklayer.CustomNetworkProtocol import CustomNetworkProtocol as NWProtoObj


##################################
#   Router class
##################################
class Router():
    '''Router'''

    ########################################
    # constructor
    ########################################
    def __init__(self):
        self.router_obj = None

    ########################################
    # configure/initialize
    ########################################
    def initialize(self, args):
        ''' Initialize the object '''

        try:
            # Here we initialize any internal variables
            print("Router Object: Initialize")

            # Now, get the configuration object
            config = configparser.ConfigParser()
            config.read(args.config)

            # Next, obtain the custom application protocol object
            self.router_obj = NWProtoObj()

            # initialize the custom application objects
            self.router_obj.initialize_router(config, args.myaddr, args.myport, args.nexthopaddr, args.nexthopport
                                            )

        except Exception as e:
            raise e


##################################
# Command line parsing
##################################
def parseCmdLineArgs():
    # parse the command line
    parser = argparse.ArgumentParser()

    # add optional arguments
    parser.add_argument("-c", "--config", default="config.ini", help="configuration file (default: config.ini")
    parser.add_argument("-a", "--myaddr", default="*", help="Interface to bind to (default: *)")
    parser.add_argument("-p", "--myport", type=int, default=4444, help="Port to bind to (default: 4444)")
    parser.add_argument("-A", "--nexthopaddr", default="127.0.0.1",
                        help="IP Address of next router or end server to connect to (default: localhost i.e., 127.0.0.1)")
    parser.add_argument("-P", "--nexthopport", type=int, default=5555,
                        help="Port that appln or next router is listening on (default: 4444)")
    parser.add_argument("-t", "--demux_token", default="router",
                        help="Our identity used as a demultiplexing token (default: router)")
    args = parser.parse_args()

    return args


# ------------------------------------------
# main function
def main():
    """ Main program """

    print("Demo program for TCP Router with ZeroMQ")

    # first parse the command line args
    parsed_args = parseCmdLineArgs()

    # Obtain a health status server object
    print("GroceryOrder main: obtain the object")
    rt = Router()

    # initialize our refrigerator object
    print("GroceryOrder main: initialize the object")
    rt.initialize(parsed_args)


# ----------------------------------------------
if __name__ == '__main__':
    # here we just print the version numbers
    print("Current libzmq version is %s" % zmq.zmq_version())
    print("Current pyzmq version is %s" % zmq.pyzmq_version())

    main()
