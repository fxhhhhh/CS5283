# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Purpose: Provides the skeleton code for our custom transport protocol
#          For assignment 1, this will be a No-Op. But we keep the layered
#          architecture in all the assignments
#

# import the needed packages
import os  # for OS functions
import sys  # for syspath and system exception
import time

# add to the python system path so that packages can be found relative to
# this directory
sys.path.insert(0, "../")

from networklayer.CustomNetworkProtocol import CustomNetworkProtocol as NWProtoObj


############################################
#  Bunch of Transport Layer Exceptions
#
# @TODO@ Add more, if these are not enough
############################################

############################################
#       Custom Transport Protocol class
############################################
class CustomTransportProtocol():
    '''Custom Transport Protocol'''

    ###############################
    # constructor
    ###############################
    def __init__(self, role):
        self.role = role  # indicates if we are client = 2 or server = 1,router = 3
        self.ip = None
        self.port = None
        self.nw_obj = None  # handle to our underlying network layer object
        self.serverCnt = 0

    ###############################
    # configure/initialize
    ###############################
    def initialize(self, config, ip, port):
        ''' Initialize the object '''

        try:
            # Here we initialize any internal variables
            print("Custom Transport Protocol Object: Initialize")

            # initialize our variables
            self.ip = ip
            self.port = port

            # in a subsequent assignment, we will use the max segment size for our
            # transport protocol. This will be passed in the config.ini file.
            # Right now we do not care.

            # Now obtain our network layer object
            print("Custom Transport Protocol::initialize - obtain network object")
            self.nw_obj = NWProtoObj()

            # initialize it
            #
            # In this assignment, we let network layer (which holds all the ZMQ logic) to
            # directly talk to the remote peer. In future assignments, this will be the
            # next hop router to whom we talk to.
            print("Custom Transport Protocol::initialize - initialize network object")
            self.nw_obj.initialize(config, self.role, self.ip, self.port)

        except Exception as e:
            raise e  # just propagate it

    #########################################  used for response  #################################################
    def send_appln_msg_responseOnly(self, payload, size):
        try:
            # @TODO@ Implement this
            # What we should get here is a serialized message from the application
            # layer along with the payload size. Now, depending on what is the
            # maximum segment size allowed by our transport, we will need to break the
            # total message into chunks of segment size and send segment by segment.
            # But we will do all this when we are implementing our custom transport
            # protocol. For Assignment #1, we send the entire message as is in a single
            # segment

            print("Custom Transport Protocol::send_appln_msg")

            self.send_segment_responseOnly(payload, size)
        except Exception as e:
            raise e

    def send_segment_responseOnly(self, segment, len=0):
        try:
            # For this assignment, we ask our dummy network layer to
            # send it to peer. We ignore the length in this assignment
            print("Custom Transport Protocol::send_segment")
            self.nw_obj.send_packet(segment, len)

        except Exception as e:
            raise e

    def recv_appln_msg_onlyForClient(self, len=0):
        try:
            # The transport protocol (at least TCP) is byte stream, which means it does not
            # know the boundaries of the message. So it must be told how much to receive
            # to make up a meaningful message. In reality, a transport layer will receive
            # all the segments that make up a meaningful message, assemble it in the correct
            # order and only then pass it up to the caller.
            #
            # For this assignment, we do not care about all these things.
            print("Custom Transport Protocol::recv_appln_msg")
            appln_msg = self.recv_segment_onlyForClient()
            return appln_msg

        except Exception as e:
            raise e

        ######################################
        #  receive transport segment
        ######################################

    def recv_segment_onlyForClient(self, len=0):
        try:
            # receive a segment. In future assignments, we may be asking for
            # a pipeline of segments.
            #
            # For this assignment, we do not care about all these things.
            print("Custom Transport Protocol::recv_segment")
            segment = self.nw_obj.recv_packet(len)
            return segment

        except Exception as e:
            raise e


    ########################################  used for respons  e#####################################################




    ##################################
    #  send application message
    ##################################
    def send_appln_msg(self, payload, size):
        try:
            # @TODO@ Implement this
            # What we should get here is a serialized message from the application
            # layer along with the payload size. Now, depending on what is the
            # maximum segment size allowed by our transport, we will need to break the
            # total message into chunks of segment size and send segment by segment.
            # But we will do all this when we are implementing our custom transport
            # protocol. For Assignment #1, we send the entire message as is in a single
            # segment

            print("Custom Transport Protocol::send_appln_msg")

            self.send_segment(payload, size)
        except Exception as e:
            raise e



    ########################################  used for AB  e#####################################################
    ##################################
    #  send transport layer segment AB
    ##################################
    def send_segment(self, segment, len=0):
        try:
            # For this assignment, we ask our dummy network layer to
            # send it to peer. We ignore the length in this assignment
            print("Custom Transport Protocol::send_segment")
            ip = segment[0:8]
            length = segment[8:11]
            msg = segment[11:]
            signal = 0
            for i in range(0, 65):
                currChunk = ip + length + msg[i * 16: (i + 1) * 16] + bytes(str(signal % 2), 'utf-8')
                print(currChunk)
                self.nw_obj.send_packet(currChunk, len)





                currRecv = self.nw_obj.recv_packet()
                print("---------the ack I have received----------")
                print(type(currRecv))
                print(currRecv.decode('utf-8'))
                print("---------the ack I have received----------")
                currRecv = int(currRecv.decode("utf-8"))
                # used to check if I receive the correct ack
                while currRecv != signal % 2:
                    self.nw_obj.send_packet(currChunk, len)
                    currRecv = self.nw_obj.recv_packet()
                    currRecv = int(currRecv.decode("utf-8"))
                signal += 1
            # work as the end signal for whole message
            self.nw_obj.send_packet(ip + length + bytes(str('3'),'utf-8'), 12)
            print('finish sending the information by segment')
        except Exception as e:
            raise e

    ######################################
    #  receive application-level message
    ######################################
    def recv_appln_msg(self, len1=0):
        try:
            # The transport protocol (at least TCP) is byte stream, which means it does not
            # know the boundaries of the message. So it must be told how much to receive
            # to make up a meaningful message. In reality, a transport layer will receive
            # all the segments that make up a meaningful message, assemble it in the correct
            # order and only then pass it up to the caller.
            #
            # For this assignment, we do not care about all these things.
            print("Custom Transport Protocol::recv_appln_msg")
            res_appln_msg = b''
            print('debug 1')
            size = 0
            currMsg = ''
            while currMsg != 3:
                currMsg = self.recv_segment()
                print("-------------curr Msg ----------------")
                print(currMsg)
                print("-------------curr Msg ----------------")
                if(currMsg == 3):
                    break
                if(currMsg == b''):
                    continue
                print(currMsg[8:11])
                size = int(currMsg[8:11].decode("utf-8"))
                res_appln_msg = res_appln_msg[:-1] + currMsg[11:]
                print("-------------curr received msg ----------------")
                print(res_appln_msg)
                print("-------------curr received msg ----------------")
            res_appln_msg = res_appln_msg[0:size]
            print(res_appln_msg)
            print(len(res_appln_msg))
            print("Custom Transport Protocol::recv_appln_msg -------- successfully")
            return res_appln_msg

        except Exception as e:
            raise e

    ######################################
    #  receive transport segment
    ######################################
    def recv_segment(self, len=0):
        try:
            # receive a segment. In future assignments, we may be asking for
            # a pipeline of segments.
            #
            # For this assignment, we do not care about all these things.
            print("Custom Transport Protocol::recv_segment")
            segment = self.nw_obj.recv_packet()
            print(segment)
            incomingSignal = int(chr(segment[-1]))
            print("----------debug what the incoming signal is--------------")
            print(incomingSignal)
            print("----------debug what the incoming signal is--------------")
            if incomingSignal == self.serverCnt:
                print(bytes(str(self.serverCnt), 'utf-8'))
                print("----------debug what the serverCnt is--------------")
                print(self.serverCnt)
                self.nw_obj.send_packet(bytes(str(int(self.serverCnt)), 'utf-8'), 1)
                self.serverCnt = (self.serverCnt + 1) % 2
                print(segment)
                print("Custom Transport Protocol::recv_segment------ successfully")
                print(bytes(str(self.serverCnt), 'utf-8'))
                return segment
            elif incomingSignal != 3:
                print("----------send the wrong msg-------------")
                self.nw_obj.send_packet(bytes(str(int((self.serverCnt + 1) % 2)), 'utf-8'), 1)
                return b''
            else:
                print("already in the last point")
                self.serverCnt = 0
                return 3


        except Exception as e:
            raise e


    # ########################################  used for Back-N  e#####################################################
    # def send_segment(self, segment, len=0):
    #     try:
    #         # For this assignment, we ask our dummy network layer to
    #         # send it to peer. We ignore the length in this assignment
    #         print("Custom Transport Protocol::send_segment")
    #         ip = segment[0:8]
    #         length = segment[8:11]
    #         print(ip)
    #         print(length)
    #         msg = segment[11:]
    #         print(msg)
    #         signal = 0
    #         for i in range(0, 65):
    #             currChunk = ip + length + msg[i * 16: (i + 1) * 16] + bytes(str(signal % 2), 'utf-8')
    #             print(currChunk)
    #             self.nw_obj.send_packet(currChunk, len)
    #             currRecv = self.nw_obj.recv_packet()
    #             print(currRecv)
    #             currRecv = int(currRecv.decode("utf-8"))
    #             # used to check if I receive the correct ack
    #             while currRecv != signal % 2:
    #                 self.nw_obj.send_packet(currChunk, len)
    #                 currRecv = self.nw_obj.recv_packet()
    #                 currRecv = int(currRecv)
    #             signal += 1
    #         # work as the end signal for whole message
    #         self.nw_obj.send_packet(ip + length + bytes(str('3'),'utf-8'), 12)
    #         print('finish sending the information by segment')
    #     except Exception as e:
    #         raise e
