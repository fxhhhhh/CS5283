import configparser  # for configuration parsing
if __name__ == '__main__':
    a = '10.0.0.7'
    b = len(a)
    c = bytes(a,'utf-8')
    d = bytes(str(b),'utf-8')
    print(c + d)
