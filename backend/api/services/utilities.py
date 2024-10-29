import base64

def flattenList(matrix):
    flatList = []
    for row in matrix:
        flatList.extend(row)
    return flatList

def base64Encoder(string):
    return str(base64.b64encode(bytes(string, 'ascii')), 'ascii')

def base64Decoder(string):
    return str(base64.b64decode(string).decode('utf-8'))