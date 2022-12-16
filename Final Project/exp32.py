from ryu.base import app_manager
from ryu.controller.handler import set_ev_cls
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER,CONFIG_DISPATCHER,DEAD_DISPATCHER
from ryu.lib.packet import packet,ethernet
from ryu.lib.packet import arp
from ryu.lib.packet import lldp
from ryu.lib.packet import ipv4
from ryu.lib.packet import tcp
from ryu.topology import event
from ryu.topology.api import get_switch,get_link
from ryu.lib.packet import ether_types
from ryu.ofproto import ofproto_v1_3
from ryu.base.app_manager import lookup_service_brick
from ryu.topology import switches
from collections import defaultdict

import networkx as nx

boardcast = "ff:ff:ff:ff:ff:ff"

class MyShortestForwarding(app_manager.RyuApp):

    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self,*args,**kwargs):
        super(MyShortestForwarding,self).__init__(*args,**kwargs)

        #set data structor for topo construction
        self.network = nx.DiGraph()        #store the dj graph
        self.paths = {} #store the shortest path
        self.datapaths = defaultdict(lambda: None)
        self.topology_api_app = self
        self.avoid={}
        self.mac_to_port = {}
        self.ip_to_mac = {}
        self.mac_to_dpid = {}
        self.check_ip_dpid = defaultdict(list)
        self.ip_to_switch = {}
        self.port_name_to_num = {}
        self.ip_to_port = {}
        self.lldp_delay={}
        self.switches=None
        self.shortdelay=0
        self.lldp_mark={}

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures,CONFIG_DISPATCHER)
    def switch_features_handler(self,ev):
        '''
        manage the initial link between switch and controller
        '''
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        ofp_parser = datapath.ofproto_parser

        match = ofp_parser.OFPMatch()    #for all packet first arrive, match it successful, send it ro controller
        actions  = [ofp_parser.OFPActionOutput(
                            ofproto.OFPP_CONTROLLER,ofproto.OFPCML_NO_BUFFER
                            )]

        self.add_flow(datapath, 0, match, actions)

    def add_flow(self,datapath,priority,match,actions):
        '''
        fulfil the function to add flow entry to switch
        '''
        ofproto = datapath.ofproto
        ofp_parser = datapath.ofproto_parser

        inst = [ofp_parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,actions)]

        mod = ofp_parser.OFPFlowMod(datapath=datapath,priority=priority,match=match,instructions=inst)

        datapath.send_msg(mod)


    @set_ev_cls(ofp_event.EventOFPPacketIn,MAIN_DISPATCHER)
    def packet_in_handler(self,ev):
        '''
        manage the packet which comes from switch
        '''
        #first get event infomation
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        ofp_parser = datapath.ofproto_parser

        in_port = msg.match['in_port']
        dpid = datapath.id

        #second get ethernet protocol message
        pkt = packet.Packet(msg.data)
        eth_pkt = pkt.get_protocol(ethernet.ethernet)

        eth_src = eth_pkt.src  # note: mac info willn`t  change in network
        eth_dst = eth_pkt.dst


        if eth_pkt.ethertype == ether_types.ETH_TYPE_LLDP:
            if (dpid,eth_src) in self.lldp_mark:
                return
            else:
                self.lldp_mark[(dpid,eth_src)]=1
            try:
                src_dpid, src_port_no = switches.LLDPPacket.lldp_parse(msg.data)
                if self.switches is None:
                    self.switches = lookup_service_brick('switches')
                for port in self.switches.ports.keys():
                    if src_dpid == port.dpid and src_port_no == port.port_no:
                        self.lldp_delay[(src_dpid, dpid)] =self.switches.ports[port].delay
                        self.network.edges[src_dpid, dpid]['weight']=self.switches.ports[port].delay
                        self.logger.info(self.switches.ports[port].delay)
                return
            except:
                return

        if eth_pkt.ethertype == ether_types.ETH_TYPE_IPV6:
            return

        #self.logger.info("packet in %s %s %s %s", dpid, eth_src,eth_dst, in_port)

        pkt_arp = pkt.get_protocol(arp.arp)
        pkt_ipv4 = pkt.get_protocol(ipv4.ipv4)
        pkt_tcp = pkt.get_protocol(tcp.tcp)

        self.avoid.setdefault(dpid, {})
        self.avoid[dpid].setdefault(eth_src,{})

        '''
        if pkt_arp and pkt_arp.opcode == arp.ARP_REQUEST and eth_dst==boardcast:
            self.logger.info("hongfan ARP")
            if pkt_arp.dst_ip not in self.avoid[dpid][eth_src]:
                self.avoid[dpid][eth_src][pkt_arp.dst_ip] = in_port
            elif self.avoid[dpid][eth_src][pkt_arp.dst_ip] != in_port:
                return
        '''

        if pkt_arp and pkt_arp.opcode == arp.ARP_REQUEST:
            if pkt_arp.src_ip not in self.ip_to_mac:
                self.ip_to_mac[pkt_arp.src_ip] = eth_src
                self.mac_to_dpid[eth_src] = (dpid, in_port)
                self.ip_to_port[pkt_arp.src_ip] = (dpid, in_port)

            if pkt_arp.dst_ip in self.ip_to_mac:
                self.logger.info("[PACKET] ARP packet_in.")
                self.handle_arpre(datapath=datapath, port=in_port,
                                  src_mac=self.ip_to_mac[pkt_arp.dst_ip],
                                  dst_mac=eth_src, src_ip=pkt_arp.dst_ip, dst_ip=pkt_arp.src_ip)
            else:
                # to avoid flood when the dst ip not in the network
                if datapath.id not in self.check_ip_dpid[pkt_arp.dst_ip]:
                    self.check_ip_dpid[pkt_arp.dst_ip].append(datapath.id)
                    out_port = ofproto.OFPP_FLOOD
                    actions = [ofp_parser.OFPActionOutput(out_port)]
                    data = None
                    if msg.buffer_id == ofproto.OFP_NO_BUFFER:
                        data = msg.data
                    out = ofp_parser.OFPPacketOut(datapath=datapath, buffer_id=msg.buffer_id,
                                              in_port=in_port, actions=actions, data=data)
                    datapath.send_msg(out)
            return

        elif pkt_arp and pkt_arp.opcode == arp.ARP_REPLY:
            if pkt_arp.src_ip not in self.ip_to_mac:
                self.ip_to_mac[pkt_arp.src_ip] = eth_src
                self.mac_to_dpid[eth_src] = (dpid, in_port)
                self.ip_to_port[pkt_arp.src_ip] = (dpid, in_port)
            dst_mac = self.ip_to_mac[pkt_arp.dst_ip]
            (dst_dpid, dst_port) = self.mac_to_dpid[dst_mac]
            self.handle_arpre(datapath=self.datapaths[dst_dpid], port=dst_port, src_mac=eth_src, dst_mac=dst_mac,
                              src_ip=pkt_arp.src_ip, dst_ip=pkt_arp.dst_ip)
            return


        self.mac_to_port.setdefault(dpid, {})
        self.mac_to_port[dpid].setdefault(eth_src,in_port)

        if eth_dst in self.mac_to_port[dpid]:
            #self.logger.info("NOT OFPP_FLOOD")
            out_port = self.mac_to_port[dpid][eth_dst]
        else:
            #self.logger.info("OFPP_FLOOD")
            out_port = ofproto.OFPP_FLOOD

        out_port_s = out_port
        out_port = self.get_out_port(datapath,eth_src,eth_dst,in_port)
        if out_port == 555:
            return
        if out_port == ofproto.OFPP_FLOOD and out_port_s != ofproto.OFPP_FLOOD:
            out_port = out_port_s
        actions = [ofp_parser.OFPActionOutput(out_port)]
        if out_port != ofproto.OFPP_FLOOD:
            match = ofp_parser.OFPMatch(in_port=in_port, eth_dst=eth_dst)
            self.add_flow(datapath, 1, match,actions)

        out = ofp_parser.OFPPacketOut(
                datapath=datapath, buffer_id=msg.buffer_id, in_port=in_port,
                actions=actions, data=msg.data
            )

        datapath.send_msg(out)

    def send_pkt(self, datapath, port, pkt):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        pkt.serialize()
        data = pkt.data
        actions = [parser.OFPActionOutput(port=port)]
        out = parser.OFPPacketOut(datapath=datapath, buffer_id=ofproto.OFP_NO_BUFFER, in_port=ofproto.OFPP_CONTROLLER,
                                  actions=actions, data=data)
        datapath.send_msg(out)

    def handle_arpre(self, datapath, port, src_mac, dst_mac, src_ip, dst_ip):
        pkt = packet.Packet()
        pkt.add_protocol(ethernet.ethernet(ethertype=0x0806, dst=dst_mac, src=src_mac))
        pkt.add_protocol(arp.arp(opcode=arp.ARP_REPLY, src_mac=src_mac, src_ip=src_ip, dst_mac=dst_mac, dst_ip=dst_ip))
        self.send_pkt(datapath, port, pkt)

    @set_ev_cls(event.EventSwitchEnter,[CONFIG_DISPATCHER,MAIN_DISPATCHER])    #event is not from openflow protocol, is come from switchs` state changed, just like: link to controller at the first time or send packet to controller
    def get_topology(self,ev):
        #store nodes info into the Graph
        self.logger.info("GRAPH")
        switch_list = get_switch(self.topology_api_app,None)    #------------need to get info,by debug
        switches = [switch.dp.id for switch in switch_list]
        self.network.add_nodes_from(switches)

        #store links info into the Graph
        link_list = get_link(self.topology_api_app,None)
        #port_no, in_port    ---------------need to debug, get diffirent from  both
        for link in link_list:
            if (link.src.dpid,link.dst.dpid) in self.lldp_delay:
                self.network.add_edge(link.src.dpid, link.dst.dpid, weight=self.lldp_delay[(link.src.dpid,link.dst.dpid)], port=link.src.port_no)
            else:
                self.network.add_edge(link.src.dpid, link.dst.dpid,
                                      weight=1, port=link.src.port_no)
            if (link.dst.dpid,link.src.dpid) in self.lldp_delay:
                self.network.add_edge(link.dst.dpid, link.src.dpid,
                                      weight=self.lldp_delay[(link.dst.dpid, link.src.dpid)], port=link.dst.port_no)
            else:
                self.network.add_edge(link.dst.dpid, link.src.dpid, weight=1, port=link.dst.port_no)

    @set_ev_cls(ofp_event.EventOFPStateChange, [MAIN_DISPATCHER, DEAD_DISPATCHER])
    def state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if datapath.id not in self.datapaths:
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                del self.datapaths[datapath.id]

    def get_out_port(self,datapath,src,dst,in_port):
        '''
        datapath: is current datapath info
        src,dst: both are the host info
        in_port: is current datapath in_port
        '''

        dpid = datapath.id

        #the first :Doesn`t find src host at graph
        if src not in self.network:
            self.network.add_node(src)
            self.network.add_edge(dpid, src, weight=0.0,port=in_port)
            self.network.add_edge(src, dpid,weight=0.0)
            self.paths.setdefault(src, {})

        #second: search the shortest path, from src to dst host
        if src in self.network and dst in self.network:
            #self.logger.info("find")
            if dst not in self.paths[src]:    #if not cache src to dst path,then to find it
                path = nx.shortest_path(self.network,src,dst,weight="weight")
                self.shortdelay= nx.shortest_path_length(self.network, src, dst, weight="weight")
                self.paths[src][dst]=path

            path = self.paths[src][dst]
            self.shortdelay = nx.shortest_path_length(self.network, src, dst, weight="weight")
            if dpid not in path:
                return 555
            next_hop = path[path.index(dpid)+1]
            out_port = self.network[dpid][next_hop]['port']
            if next_hop==dst:
                self.logger.info("total path delay: %s",self.shortdelay)
                #print "all delay is", shortdelay

            #get path info
            self.logger.info("path : %s", str(path))
        else:
            #self.logger.info("not find")
            out_port = datapath.ofproto.OFPP_FLOOD    #By flood, to find dst, when dst get packet, dst will send a new back,the graph will record dst info
            #print("8888888888 not find dst")
        return out_port
