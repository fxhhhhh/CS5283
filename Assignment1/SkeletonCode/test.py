import configparser  # for configuration parsing
if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read('config.ini')
    config['Network']['nextAddr'] = '10.0.0.1'
    config['Network']['nextPort'] = '2222'
    with open('config.ini', 'w') as configfile: config.write(configfile)