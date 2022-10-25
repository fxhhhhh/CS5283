import configparser  # for configuration parsing
if __name__ == '__main__':
    a = bytes('10.0.0.1','utf-8')
    b = bytes('abd','utf-8')
    print(a + b)
    c = a + b
    print(c[0])
    print(c.decode('utf-8'))
    print(c.decode('utf-8')[0:8])