import configparser  # for configuration parsing
if __name__ == '__main__':
    print("Custom Transport Protocol::recv_appln_msg")
    appln_msg = bytes('', 'utf-8')

    size = 1
    while len(appln_msg) < 64 * (16 + 1 + 11) + 11:
        print('debug 1')
        currMsg = b'1234567890'
        size = int(currMsg[8:11].decode("utf-8"))
        appln_msg = appln_msg + currMsg[11:-1]
    appln_msg = appln_msg[0:size + 1]
    print("Custom Transport Protocol::recv_appln_msg -------- successfully")


