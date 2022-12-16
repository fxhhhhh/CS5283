from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from collections import defaultdict
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.topology import event
from ryu.controller.handler import MAIN_DISPATCHER,CONFIG_DISPATCHER
from ryu.controller.handler import set_ev_cls

from ryu.topology.api import get_switch,get_all_link,get_link
import copy
import random
from ryu.lib.packet import arp
from ryu.lib.packet import ipv6
from ryu.lib import mac

import numpy as np

import networkx as nx

import matplotlib.pyplot as plt

class Topo(object):
    def __init__(self,logger):
        # adjacent dict (s1,s2)->(port,weight)
        # for example, the topology we have:
        # port1---switch1---port2-----port3---switch2---port4
        # then the adjacent dict={(switch1,switch2):(port2,weight)(switch2,switch1):(port3,weight)}
        

        self.adjacent=defaultdict(lambda switch1switch2:None)
        
        self.switches=None

        # a map to record host_mac->(switch,inport)
        
        # and an additional map to record the controller's mac_to_port
        

        self.logger=logger
    
        
    
    #setting the adjacent edges in the graph
    def set_adjacent(self,switch1,switch2,port,weight):
        self.adjacent[(switch1,switch2)]=(port,weight)
    
    #initialing the graph by adding the topology information to the matrix
    def count_graph(self):
        mat = np.array(np.ones((10,10))*10000)

        for (s,t) in self.adjacent.keys():
            mat[s-1][t-1] = random.randint(1,10)
            mat[t-1][s-1] = mat[s-1][t-1]
            #print(mat)

        return mat

    #counting the number of nodes
    def count_nodenum(self,mat):
        return len(mat)

    #counting the number of edges
    def count_edgenum(self,mat):
        count = 0
        for i in range(len(mat)):
            for j in range(i):
                if mat[i][j] > 0 and mat[i][j] < 10000:
                    count += 1
    
        return count

    #implementing the Kruskal algorithm
    def kruskal(self, mat):
        nodenum = self.count_nodenum(mat)
        edgenum = self.count_edgenum(mat)

        result_array = []
        #If the number of points is negative, or the number of edges is less than the number of points -1, that is, it is not fully connected, 
        #then return directly
        if nodenum <= 0 or edgenum < nodenum - 1:
            return result_array

        #create edge collection
        edge_array = []
        #traverse the nodes
        for i in range(nodenum):
            #Starting from i, traverse the rest of the points
            for j in range(i+1, nodenum):
                
                #If there is an edge between two nodes
                if mat[i][j] < 10000:
                    #Add the edge to the set in the form of [node i, node j, weight]
                    edge_array.append([i, j, mat[i][j]])

        #Sort the edges
        edge_array.sort(key=lambda a: a[2])

        #Create node list
        group = [[i] for i in range(nodenum)]
        #for each edge
        for edge in edge_array:
            for i in range(len(group)):
                if edge[0] in group[i]:
                    a = i
                if edge[1] in group[i]:
                    b = i
            if a != b:
                result_array.append(edge)
                group[a] = group[a] + group[b]
                group[b] = []
        
        return result_array
    
    
    def compute_plot(self):
        mat = self.count_graph()
        link_array1 = self.kruskal(mat)
        
        #print('src:',src_dw)
        for i in link_array1:
            print(i[0]+1, ' to ', i[1]+1, '   weight = ', i[2])
        
        print('link array:',link_array1)
        
        #link_array2=link_array1
        #for i in link_array2:
            #i[0]+=1
            #i[1]+=1
        #print('linkList:',link_array2)
        
        
        # plotting the graph
        Graphh=nx.Graph()  
 
        # links records all links in the Kruskal graph
        links=[]
        
        # Kruslinks records all the Kruskal links after the computation
        Kruslinks=[]
        # weight is a dictionary that stores the weights between every two nodes
        weight={}
        for i in range(len(mat)):
            for j in range(i):
                if mat[i][j] > 0 and mat[i][j] < 10000:
                    links.append((i+1,j+1))
                    links.append((j+1,i+1))
                    weight[(i+1,j+1)]=mat[i][j]
                    weight[(j+1,i+1)]=mat[i][j]
        print('\n\n',weight,'\n\n')
        print(links,'\n\n')
        
        
        for lin in links:
            Graphh.add_edge(lin[0],lin[1],color='black')
            
            
            
            
        for link1 in link_array1:
            Kruslinks.append((link1[0]+1,link1[1]+1))
            Kruslinks.append((link1[1]+1,link1[0]+1))
     
        print(Kruslinks)
        
        for krusl in Kruslinks:
            Graphh.add_edge(krusl[0],krusl[1],color='g')

        #elargse=[(u,v) for (u,v,d) in Graphh.edges(data=True)]
        layoutt=nx.spring_layout(Graphh)
        edges = Graphh.edges()
        colors = [Graphh[u][v]['color'] for u,v in edges]
        nx.draw_networkx_nodes(Graphh,layoutt,node_size=700)
        #nx.draw_networkx_edges(Graphh,layoutt,width=3,edge_color=colors)
        
        nx.draw_networkx_labels(Graphh,layoutt,font_size=20)

        
        nx.draw_networkx_edge_labels(Graphh,layoutt,weight,font_size=15)
        
       
        plt.show()
        result = []
        return result
        #end of the plotting

   

class MyController(app_manager.RyuApp):
    #Define the OpenFlow version
    OFP_VERSIONS=[ofproto_v1_3.OFP_VERSION]

    def __init__(self,*args,**kwargs):
        super(MyController,self).__init__(*args,**kwargs)
        
        
        #the global mac-port table,{{datapath:mac->port},...,{datapath:mac->port}}
        self.mac_to_port={}
        
        #record of all datapath
        self.datapaths=[]
        
        #flood history table
        self.flood_history={}        

        self.flag = False
        
        self.topo = Topo(self.logger)

    #Features_Response_Received
    # defining event handler for setup and configuring of switches
    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, ev):
    
        # getting the datapath, ofproto and parser objects of the event
        
        #ev.msg: Each event class ev has a msg member, which is used to carry the data packet that triggers the event.
        #msg.datapath: The formatted msg is actually a packet_in message, and msg.datapath can directly obtain the datapath structure of the packet_in message.
        datapath = ev.msg.datapath
        
        #The datapath.ofproto object is an object of the OpenFlow protocol data structure, and its members include the data structure of the OpenFlow protocol,
        #such as the action type OFPP_FLOOD.
        ofproto = datapath.ofproto
        #datapath.ofp_parser is a data structure parsed according to OpenFlow.
        parser = datapath.ofproto_parser

        # install table-miss flow entry

        #This match is with no match fields. it means matching all the packets.
        match = parser.OFPMatch()
        
        #Actions is a list for storing action list, where actions can be added
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)
    
    def add_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        #Create a Instruction list with Actions
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        
        #Send OFP Flow Modifiation meassage for creating a new flow
        #Most of the parameter are default.
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)


    
    #PacketIn_Message_Received
    @set_ev_cls(ofp_event.EventOFPPacketIn,MAIN_DISPATCHER)
    def packet_in_handler(self,event):
        msg=event.msg
        datapath=msg.datapath
        ofproto=datapath.ofproto
        parser=datapath.ofproto_parser

        # through which port the packet comes in
        in_port=msg.match['in_port']

        #creating a packet encoder/decoder class with the raw data obtained by msg
        pkt=packet.Packet(msg.data)
        #getting the protocl that matches the received packet
        eth=pkt.get_protocols(ethernet.ethernet)[0]
        
        
        #implementing the kruskal algorithm and the plotting
        if self.flag == False:
            path = self.topo.compute_plot()
                
                
            self.flag = True
                   
        
        #avoid broadcasts from LLDP
        if eth.ethertype==ether_types.ETH_TYPE_LLDP:
            #self.logger.info("LLDP")
            return

        #getting the mac_addr information
        dst_mac=eth.dst

        src_mac=eth.src

 
    
    #A switch joins the network
    @set_ev_cls(event.EventSwitchEnter)
    def switch_enter_handler(self,event):
        self.logger.info("A switch entered.Topology rediscovery...")
        self.switch_status_handler(event)
        self.logger.info('Topology rediscovery done')
    
    @set_ev_cls(event.EventSwitchLeave)
    def switch_leave_handler(self,event):
        self.logger.info("A switch leaved.Topology rediscovery...")
        self.switch_status_handler(event)
        self.logger.info('Topology rediscovery done')



    def switch_status_handler(self,event):

       

        # use copy to avoid unintended modification which is fatal to the network
        all_switches=copy.copy(get_switch(self,None))
       

        
        #getting the ID of teh switch
        self.topo.switches=[s.dp.id for s in all_switches]

        self.logger.info("switches {}".format(self.topo.switches))
        
        # getting all datapathid
        self.datapaths=[s.dp for s in all_switches]

        # getting all links  
        all_links=copy.copy(get_link(self,None))
        
        # link port 1,port 2

        all_link_data=[(l.src.dpid,l.dst.dpid,l.src.port_no,l.dst.port_no) for l in all_links]
        self.logger.info("Number of links {}".format(len(all_link_data)))

        #all links's information
        all_link_list=''


        for switch1,switch2,port1,port2 in all_link_data:
            
            
            # in RYU, it's like switch1---->switch2,switch2---->switch1
            # after all enumerations, the latter one overrides the previous one
            weight=random.randint(1,6)

            self.topo.set_adjacent(switch1,switch2,port1,weight)
            self.topo.set_adjacent(switch2,switch1,port2,weight)

            all_link_list+='s{}p{}--s{}p{}\n'.format(switch1,port1,switch2,port2)
        self.logger.info("All links:\n "+all_link_list)
    

