# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Purpose: Provides the skeleton code for our custom network protocol
#          For assignment 1, this will be very simple and will include
#          all the ZeroMQ logic
#

# import the needed packages
import os  # for OS functions
import sys  # for syspath and system exception
import random

# add to the python system path so that packages can be found relative to
# this directory
sys.path.insert(0, "../")

# import the zeromq capabilities
import zmq


############################################
#  Bunch of Network Layer Exceptions
#
# @TODO@ Add whatever make sense here.
############################################

############################################
#       Custom Network Protocol class
############################################
class CustomNetworkProtocol():
    '''Custom Network Protocol'''

    ###############################
    # constructor
    ###############################
    def __init__(self):
        self.role = None  # indicates if we are client or server, false => client
        self.config = None  # network configuration
        self.ctx = None  # ZMQ context
        self.socket = None  # At this stage we do not know if more than one socket needs to be maintained
        self.poller = None

    ###############################
    # configure/initialize
    ###############################
    def initialize(self, config, role, ip, port):
        ''' Initialize the object '''

        try:
            # Here we initialize any internal variables
            print("Custom Network Protocol Object: Initialize")
            self.config = config
            self.role = role
            self.ip = ip
            self.port = port

            # initialize our variables
            print("Custom Network Protocol Object: Initialize - get ZeroMQ context")
            self.ctx = zmq.Context()

            # initialize the config object

            # initialize our ZMQ socket
            #
            # @TODO@
            # Note that in a subsequent assignment, we will need to move on to a
            # different ZMQ socket pair, which supports asynchronous transport. In those
            # assignments we may be using the DEALER-ROUTER pair instead of REQ-REP
            #
            # For now, we are fine.
            if (self.role):
                # we are the server side
                # print("here is the server ")
                # print("Custom Network Protocol Object: Initialize - get REP socket")
                self.socket = self.ctx.socket(zmq.REP)
                # since we are server, we bind
                bind_str = "tcp://" + self.ip + ":" + str(self.port)
                print("Custom Network Protocol Object: Initialize - bind socket to {}".format(bind_str))
                self.socket.bind(bind_str)
                # self.bind_sock = self.ctx.socket(zmq.ROUTER)
                #
                # # since we are server, we bind
                # bind_str = "tcp://" + self.ip + ":" + str(self.port)
                # print("Custom Network Protocol Object: Initialize - bind socket to {}".format(bind_str))
                # self.bind_sock.bind(bind_str)
                #
                #
                # self.conn_sock = self.ctx.socket(zmq.DEALER)
                # ip = config[self.ip]['ip1']
                # port = '4444'
                # connect_str = "tcp://" + ip + ":" + str(port)
                # print("Custom Network Protocol Object: Initialize - connect socket to {}".format(connect_str))
                # self.conn_sock.connect(connect_str)

            else:
                self.poller = zmq.Poller()
                self.socket = self.ctx.socket(zmq.DEALER)
                self.socket.setsockopt(zmq.IDENTITY)
                connect_string = "tcp://" + "10.0.0.2" + ":" + str(4444)
                print("TCP client will be connecting to {}".format(connect_string))
                self.socket.connect(connect_string)
                print("Register sockets for incoming events")
                # poller.register (bind_sock, zmq.POLLIN)
                self.poller.register(self.socket, zmq.POLLIN)

                # self.socket = self.ctx.socket(zmq.REQ)
                # ip = '10.0.0.2'
                # port = '4444'
                # # since we are client, we connect
                # connect_str = "tcp://" + ip + ":" + str(port)
                # print("Custom Network Protocol Object: Initialize - connect socket to {}".format(connect_str))
                # self.socket.connect(connect_str)




                # we are the client side
                # print("Custom Network Protocol Object: Initialize - get REQ socket")
                # print("here is the client ")
                # self.bind_sock = self.ctx.socket(zmq.ROUTER)
                # # since we are server, we bind
                # ip = '10.0.0.1'
                # port = '4444'
                # bind_str = "tcp://" + ip + ":" + str(port)
                # print("Custom Network Protocol Object: Initialize - bind socket to {}".format(bind_str))
                # self.bind_sock.bind(bind_str)
                # self.conn_sock = self.ctx.socket(zmq.DEALER)
                # ip = '10.0.0.2'
                # port = '4444'
                # connect_str = "tcp://" + ip + ":" + str(port)
                # print("Custom Network Protocol Object: Initialize - connect socket to {}".format(connect_str))
                # self.conn_sock.connect(connect_str)


        except Exception as e:
            raise e  # just propagate it

    def initialize_router(self, config, myaddr, myport, nexthopaddr, nexthopport):
        ''' Initialize the object '''
        self.conn_table = {}
        try:
            # Here we initialize any internal variables
            print("Custom Network Protocol Object: Initialize")
            self.config = config
            # self.role = role
            self.myaddr = myaddr
            self.myport = myport
            self.nexthopaddr = nexthopaddr
            self.nexthopport = nexthopport

            # initialize the config object

            # initialize our ZMQ socket
            #
            # @TODO@
            # Note that in a subsequent assignment, we will need to move on to a
            # different ZMQ socket pair, which supports asynchronous transport. In those
            # assignments we may be using the DEALER-ROUTER pair instead of REQ-REP
            #
            # For now, we are fine.

            try:
                # every ZMQ session requires a context
                print("Obtain the ZMQ context")
                context = zmq.Context()  # returns a singleton object
            except zmq.ZMQError as err:
                print("ZeroMQ Error obtaining context: {}".format(err))
                return
            except:
                print("Some exception occurred getting context {}".format(sys.exc_info()[0]))
                return

            try:
                # Get a poller object
                print("Obtain the Poller")
                poller = zmq.Poller()
            except zmq.ZMQError as err:
                print("ZeroMQ Error obtaining poller: {}".format(err))
                return
            except:
                print("Some exception occurred getting poller {}".format(sys.exc_info()[0]))
                return

            try:
                # The socket concept in ZMQ is far more advanced than the traditional socket in
                # networking. Each socket we obtain from the context object must be of a certain
                # type. For TCP, we will use ROUTER for server side (many other pairs are supported
                # in ZMQ for tcp.
                print("Obtain the ROUTER type socket")
                bind_sock = context.socket(zmq.ROUTER)
            except zmq.ZMQError as err:
                print("ZeroMQ Error obtaining ROUTER socket: {}".format(err))
                return
            except:
                print("Some exception occurred getting ROUTER socket {}".format(sys.exc_info()[0]))
                return

            try:
                # as in a traditional socket, tell the system what port are we going to listen on
                # Moreover, tell it which protocol we are going to use, and which network
                # interface we are going to listen for incoming requests. This is TCP.
                print("Bind the ROUTER socket")
                bind_string = "tcp://" + self.myaddr + ":" + str(self.myport)
                print("TCP router will be binding on {}".format(bind_string))
                bind_sock.bind(bind_string)
            except zmq.ZMQError as err:
                print("ZeroMQ Error binding ROUTER socket: {}".format(err))
                bind_sock.close()
                return
            except:
                print("Some exception occurred binding ROUTER socket {}".format(sys.exc_info()[0]))
                bind_sock.close()
                return

            try:
                # register sockets
                print("Register sockets for incoming events")
                poller.register(bind_sock, zmq.POLLIN)
            except zmq.ZMQError as err:
                print("ZeroMQ Error registering with poller: {}".format(err))
                return
            except:
                print("Some exception occurred getting poller {}".format(sys.exc_info()[0]))
                return

            try:
                # collect all the sockets that are enabled in this iteration
                print("Poller polling")
                socks = dict(poller.poll())
            except zmq.ZMQError as err:
                print("ZeroMQ Error polling: {}".format(err))
                return
            except:
                print("Some exception occurred in polling {}".format(sys.exc_info()[0]))
                return
            # since we are a server, we service incoming clients forever
            print("Router now starting its forwarding loop")
            while True:
                try:
                    # collect all the sockets that are enabled in this iteration
                    print("Poller polling")
                    socks = dict(poller.poll())
                    print(self.conn_table)
                except zmq.ZMQError as err:
                    print("ZeroMQ Error polling: {}".format(err))
                    return
                except:
                    print("Some exception occurred in polling {}".format(sys.exc_info()[0]))
                    return


                # Now handle the event for each enabled socket

                if bind_sock in socks:
                    # we are here implies that the bind_sock had some info show up.
                    socks = dict(poller.poll())

                    try:
                        #  Wait for next request from previous hop. When using DEALER/ROUTER, it is suggested to use
                        # multipart send/receive. What we receive will comprise the sender's info which we must preserve, an empty
                        # byte, and then the actual payload
                        print("Receive from prev hop")
                        request = bind_sock.recv_multipart()
                        print("Router received request from prev hop via ROUTER: %s" % request)
                    except zmq.ZMQError as err:
                        print("ZeroMQ Error receiving: {}".format(err))
                        bind_sock.close()
                        return
                    except:
                        print("Some exception occurred receiving/sending {}".format(sys.exc_info()[0]))
                        bind_sock.close()
                        return

                    print("get my target position")
                    print(self.myaddr)
                    print(request)
                    msg = request[int(config[self.myaddr[7]]['a'])].decode("utf-8")[0:8]

                    if(msg in self.conn_table):
                        conn_sock = self.conn_table[msg]
                        conn_sock.send_multipart(request)
                    else:
                        try:
                            # The socket concept in ZMQ is far more advanced than the traditional socket in
                            # networking. Each socket we obtain from the context object must be of a certain
                            # type. For TCP, we will use the DEALER socket type (many other pairs are supported)
                            # and this is to be used on the client side.
                            print("Router acquiring connection socket")
                            conn_sock = context.socket(zmq.DEALER)
                        except zmq.ZMQError as err:
                            print("ZeroMQ Error obtaining context: {}".format(err))
                            return
                        except:
                            print("Some exception occurred getting DEALER socket {}".format(sys.exc_info()[0]))
                            return

                        if (int(msg[7]) == 5):
                            nexthopaddr = config[self.myaddr + ""]["ip1"]
                            nexthopport = config[self.myaddr + ""]["port1"]
                        if (int(msg[7]) == 6):
                            nexthopaddr = config[self.myaddr + ""]["ip2"]
                            nexthopport = config[self.myaddr + ""]['port2']

                        try:
                            # as in a traditional socket, tell the system what IP addr and port are we
                            # going to connect to. Here, we are using TCP sockets.
                            print("Router connecting to next hop")
                            connect_string = "tcp://" + nexthopaddr + ":" + str(nexthopport)
                            print("TCP client will be connecting to {}".format(connect_string))
                            conn_sock.connect(connect_string)
                        except zmq.ZMQError as err:
                            print("ZeroMQ Error connecting DEALER socket: {}".format(err))
                            conn_sock.close()
                            return
                        except:
                            print("Some exception occurred connecting DEALER socket {}".format(sys.exc_info()[0]))
                            conn_sock.close()
                            return

                        try:
                            # register sockets
                            # print("Register sockets for incoming events")
                            # poller.register(bind_sock, zmq.POLLIN)
                            poller.register(conn_sock, zmq.POLLIN)
                        except zmq.ZMQError as err:
                            print("ZeroMQ Error registering with poller: {}".format(err))
                            return
                        except:
                            print("Some exception occurred getting poller {}".format(sys.exc_info()[0]))
                            return

                        self.conn_table[msg] = conn_sock
                        try:
                            #  forward request to server
                            print("Forward the same request to next hop over the DEALER")
                            conn_sock.send_multipart(request)
                            print(request)
                        except zmq.ZMQError as err:
                            print("ZeroMQ Error forwarding: {}".format(err))
                            conn_sock.close()
                            return
                        except:
                            print("Some exception occurred forwarding {}".format(sys.exc_info()[0]))
                            conn_sock.close()
                            return


                if conn_sock in socks:
                    try:
                        #  Wait for response from next hop
                        print("Receive from next hop")
                        response = conn_sock.recv_multipart()
                        print("Router received response from next hop via DEALER: %s" % response)
                    except zmq.ZMQError as err:
                        print("ZeroMQ Error receiving response: {}".format(err))
                        conn_sock.close()
                        return
                    except:
                        print("Some exception occurred receiving response {}".format(sys.exc_info()[0]))
                        conn_sock.close()
                        return

                    try:
                        #  Send reply back to previous hop. request[0] is the original client identity preserved at every hop
                        # response[1] has actual payload
                        print("Send reply to prev hop via ROUTER")
                        bind_sock.send_multipart(response)
                    except zmq.ZMQError as err:
                        print("ZeroMQ Error sending: {}".format(err))
                        bind_sock.close()
                        return
                    except:
                        print("Some exception occurred receiving/sending {}".format(sys.exc_info()[0]))
                        bind_sock.close()
                        return
        except Exception as e:
            raise e  # just propagate it
    ##################################
    #  send network packet
    ##################################
    # def send_packet1(self, packet, size):
    #     try:
    #
    #         # Here, we simply delegate to our ZMQ socket to send the info
    #         print("Custom Network Protocol::send_packet")
    #         # @TODO@ - this may need mod depending on json or serialized packet
    #         print("CustomNetworkProtocol::send_packet")
    #         print(packet)
    #         ip = packet[0:8]
    #         length = packet[8:11]
    #         print(ip)
    #         print(length)
    #         for i in range(0,64):
    #             chunk = packet[11 + i * 16, 11 + i * 16 + 16]
    #             chunk = ip + length + chunk + bytes(str(i),'utf-8')
    #             self.send_packet(chunk)
    #             recv = self.recv_packet()
    #             while(int(recv.decode("utf-8")) != i):
    #                 self.send_packet(chunk)
    #
    #         #self.socket.send(bytes(packet,"utf-8"))
    #     except Exception as e:
    #         raise e

    # ##################################
    # #  send network packet
    # ##################################
    # def send_packet(self, packet, size):
    #     try:
    #
    #         # Here, we simply delegate to our ZMQ socket to send the info
    #         print("Custom Network Protocol::send_packet")
    #         # @TODO@ - this may need mod depending on json or serialized packet
    #         print("CustomNetworkProtocol::send_packet")
    #         # add the randomly generate information
    #         # randomGenerate = os.urandom(1024 - len(packet))
    #         # packet = packet + randomGenerate + bytes(len(packet),'utf-8')
    #         # print(len(packet))
    #         poller = zmq.Poller()
    #         poller.register(poller, zmq.POLLIN)
    #         socks = dict(poller.poll())
    #         if self.conn_sock in socks:
    #             self.conn_sock.send(packet)
    #
    #         # self.socket.send(bytes(packet,"utf-8"))
    #     except Exception as e:
    #         raise e
    #
    # ######################################
    # #  receive network packet
    # ######################################
    # def recv_packet(self, len=0):
    #     try:
    #         # @TODO@ Note that this method always receives bytes. So if you want to
    #         # convert to json, some mods will be needed here. Use the config.ini file.
    #         poller = zmq.Poller()
    #         poller.register(poller, zmq.POLLIN)
    #         socks = dict(poller.poll())
    #         if self.bind_sock in socks:
    #             print("CustomNetworkProtocol::recv_packet")
    #             packet = self.bind_sock.recv_multipart()[-1]
    #             print(packet)
    #             print("CustomNetworkProtocol::recv_packet ------ successfully")
    #             return packet
    #     except Exception as e:
    #         raise e
  ##################################
    #  send network packet
    ##################################
    def send_packet(self, packet, size = 0):
        try:

            # Here, we simply delegate to our ZMQ socket to send the info
            print("Custom Network Protocol::send_packet")
            # @TODO@ - this may need mod depending on json or serialized packet
            print("CustomNetworkProtocol::send_packet")
            # self.socket.send (bytes(packet, "utf-8"))
            # self.socket.send(packet)
            print(self.role)
            if self.role :
                print("The packet is SENT without any loss")
                self.socket.send(packet)
            else:
                scenario = random.randint(1, 1)
                print("------------- 3 6 9-----------------")
                print(scenario)
                print("------------- 3 6 9-----------------")
                if scenario != 0:
                    print("The packet is SENT luckily")
                    self.socket.send(packet)
                else:
                    print("The packet is DROPPED and failed to be sent")

        except Exception as e:
            raise e


    ######################################
    #  receive network packet
    ######################################
    def recv_packet(self, len=0):
        try:
            # @TODO@ Note that this method always receives bytes. So if you want to
            # convert to json, some mods will be needed here. Use the config.ini file.
            print("CustomNetworkProtocol::recv_packet")
            packet = self.socket.recv()
            print(packet)
            print("CustomNetworkProtocol::recv_packet ------ successfully")
            return packet
        except Exception as e:
            raise e

    def send_multi(self, packet, size):
        try:

            # Here, we simply delegate to our ZMQ socket to send the info
            print("Custom Network Protocol::send_multi")
            # @TODO@ - this may need mod depending on json or serialized packet
            print("CustomNetworkProtocol::send_multi")
            self.socket.send_multipart([b'', bytes(packet, "utf-8")])
            # self.conn_sock.send_multipart (bytes(packet, "utf-8"))

        except Exception as e:
            raise e


    def recv_multi(self, len=0):
        try:
            # @TODO@ Note that this method always receives bytes. So if you want to
            # convert to json, some mods will be needed here. Use the config.ini file.
            print("CustomNetworkProtocol::recv_multi")
            response = self.socket.recv_multipart()
            # response = self.conn_sock.recv_multipart ()

            return response
        except Exception as e:
            raise e
