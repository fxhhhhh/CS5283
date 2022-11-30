def getNextHop(source,destination):
    if source == '10.0.0.1' and destination == '10.0.0.5':
        return '10.0.0.2'
    if source == '10.0.0.1' and destination == '10.0.0.6':
        return '10.0.0.2'
    if source == '10.0.0.2' and destination == '10.0.0.5':
        return '10.0.0.3'
    if source == '10.0.0.2' and destination == '10.0.0.6':
        return '10.0.0.4'
    if source == '10.0.0.3' and destination == '10.0.0.5':
        return '10.0.0.2'
    if source == '10.0.0.3' and destination == '10.0.0.6':
        return '10.0.0.6'
    if source == '10.0.0.4' and destination == '10.0.0.5':
        return '10.0.0.5'
    if source == '10.0.0.4' and destination == '10.0.0.6':
        return '10.0.0.6'

