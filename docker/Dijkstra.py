# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
#
# Code taken from ZeroMQ's sample code for the HelloWorld
# program, but modified to use REQ-REP sockets to showcase
# TCP. Plus, added other decorations like comments, print statements,
# argument parsing, etc.
#
# ZMQ is also offering a new CLIENT-SERVER pair of ZMQ sockets but
# these are still in draft form and are not properly supported. If you
# want to try, just replace REQ by CLIENT here (and correspondingly, in
# the tcp_server.py, replace REP by SERVER)
#
# Note: my default indentation is now set to 2 (in other snippets, it
# used to be 4)
import configparser
# import the needed packages
import sys  # for system exception
import time  # for sleep
import argparse  # for argument parsing
import zmq  # this package must be imported for ZMQ to work


##################################
# Command line parsing
##################################
def parseCmdLineArgs():
    # parse the command line
    parser = argparse.ArgumentParser()

    # add optional arguments
    parser.add_argument("-a", "--addr", default="127.0.0.1",
                        help="IP Address of next hop router to connect to (default: localhost i.e., 127.0.0.1)")
    parser.add_argument("-p", "--port", type=int, default=4444,
                        help="Port that next hop router is listening on (default: 4444)")
    parser.add_argument("-i", "--iters", type=int, default=10, help="Number of iterations (default: 1000")
    parser.add_argument("-m", "--message", default="HelloWorld", help="Message to send: default HelloWorld")
    parser.add_argument("-t", "--demux_token", default="client",
                        help="Our identity used as a demultiplexing token (default: client)")
    parser.add_argument("-f", "--final", default="server",
                        help="set the final destination")
    parser.add_argument("-c", "--config", default="route_map.ini", help="route map")
    parser.add_argument("-l", "--latency", default="latency.ini", help="latency file")
    parser.add_argument("-r", "--route", default="final_route.ini", help=" route map ")

    args = parser.parse_args()

    return args


def normal_Dijkstra(matrix):
    matrix_length = len(matrix)
    used_node = [False] * matrix_length
    list = ['client', 'router1', 'router2', 'router3', 'router4', 'router5', 'server']
    distance = [float('inf')] * matrix_length
    approaches = []
    for i in range(matrix_length):
        approaches.append([])
    distance[0] = 0
    while used_node.count(False):
        min_value = float('inf')
        min_value_index = -1
        for index in range(matrix_length):
            if not used_node[index] and distance[index] < min_value:
                min_value = distance[index]
                min_value_index = index

        used_node[min_value_index] = True
        for index in range(matrix_length):
            if distance[index] > distance[min_value_index] + matrix[min_value_index][index]:
                distance[index] = distance[min_value_index] + matrix[min_value_index][index]
                for i in approaches[min_value_index]:
                    approaches[index].append(i)
                approaches[index].append(list[min_value_index])
            # distance[index] = min(distance[index], distance[min_value_index] + matrix[min_value_index][index])
    print(distance)
    print(approaches)
    return approaches


def generate_matrix_latency(args):
    latency = configparser.ConfigParser()
    latency.read(args.latency)
    matrix = [[float('inf')] * 7, [float('inf')] * 7, [float('inf')] * 7, [float('inf')] * 7, [float('inf')] * 7,
              [float('inf')] * 7, [float('inf')] * 7]
    index1 = 0
    list = ['client', 'router1', 'router2', 'router3', 'router4', 'router5', 'server']
    for i in list:
        index2 = 0
        for j in list:
            if index1 == index2:
                matrix[index1][index2] = 0
            else:
                for m in latency[i]:
                    if m == j:
                        matrix[index1][index2] = float(latency[i][j])
            index2 += 1
        index1 += 1
    return matrix


def generate_matrix(args):
    config = configparser.ConfigParser()
    config.read(args.config)
    matrix = [[float('inf')] * 7, [float('inf')] * 7, [float('inf')] * 7, [float('inf')] * 7, [float('inf')] * 7,
              [float('inf')] * 7, [float('inf')] * 7]
    index1 = 0
    list = ['client', 'router1', 'router2', 'router3', 'router4', 'router5', 'server']
    for i in list:
        index2 = 0
        for j in list:
            if index1 == index2:
                matrix[index1][index2] = 0
            else:
                for m in config[i]:
                    for n in config[j]:
                        if m != 'port' and n != 'port' and check_if_in_the_same_subNet(config[i][m], config[j][n]):
                            matrix[index1][index2] = 1
            index2 += 1
        index1 += 1
    return matrix


def check_if_in_the_same_subNet(a, b):
    a_ip = a.split('.')
    b_ip = b.split('.')
    if a_ip[0] == b_ip[0] and a_ip[1] == b_ip[1] and a_ip[2] == b_ip[2]:
        return True
    else:
        return False


# ------------------------------------------
# main function
def main():
    """ Main program """

    print("Demo program for TCP Client with ZeroMQ Using Intermediate routers")

    # first parse the command line args
    parsed_args = parseCmdLineArgs()

    matrix1 = generate_matrix(parsed_args)
    matrix2 = generate_matrix_latency(parsed_args)
    print(matrix1)
    print(matrix2)
    approaches = normal_Dijkstra(matrix2)
    # normal_Dijkstra(matrix2)
    config = configparser.ConfigParser()
    config.read(parsed_args.config)

    f = open(parsed_args.route, 'a')
    index = 1
    for i in approaches[len(approaches) - 1]:
        if index == 1:
            index += 1
            f.write('[{0}]\n'.format(i))
            prev = i
        else:
            for m in config[prev]:
                for n in config[i]:
                    if m != 'port' and n != 'port' and check_if_in_the_same_subNet(config[prev][m], config[i][n]):
                        f.write('myAddr = {}\n'.format(config[prev][m]))
                        f.write('myPort = {}\n'.format(config[prev]['port']))
                        f.write('addr = {}\n'.format(config[i][n]))
                        f.write('port = {}\n'.format(config[i]['port']))
            prev = i
            f.write('[{0}]\n'.format(i))
    for m in config[prev]:
        for n in config['server']:
            if m != 'port' and n != 'port' and check_if_in_the_same_subNet(config[prev][m], config['server'][n]):
                f.write('myAddr = {}\n'.format(config[prev][m]))
                f.write('myPort = {}\n'.format(config[prev]['port']))
                f.write('addr = {}\n'.format(config['server'][n] ))
                f.write('port = {}\n'.format(config['server']['port']))
                f.write('[{0}]\n'.format('server'))
                f.write('myAddr = {}\n'.format(config['server'][n] ))
                f.write('myPort = {}\n'.format(config['server']['port']))
    f.close()


# ----------------------------------------------
if __name__ == '__main__':
    # here we just print the version numbers
    print("Current libzmq version is %s" % zmq.zmq_version())
    print("Current pyzmq version is %s" % zmq.pyzmq_version())

    main()
