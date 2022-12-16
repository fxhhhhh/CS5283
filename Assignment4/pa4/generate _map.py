import argparse


def parseCmdLineArgs():
    # parse the command line
    parser = argparse.ArgumentParser()

    # add optional arguments
    parser.add_argument("-indentify", "--identity", default="client1", help="indentify current service")
    args = parser.parse_args()

    return args

def main():

    parsed_args = parseCmdLineArgs()
    service = parsed_args.identity
    f = open('route_map.ini', 'a')
    f.writelines("[{}]".format(service))
    import netifaces
    index = 0
    try:
        f.write("eth{0}={1}".format(index, netifaces.ifaddresses('eth{}'.format(index))))
        index += 1
    except:
        f.close()


if __name__ == '__main__':
    main()



