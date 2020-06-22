import base64


def encode_word(string):
    string = base64.b64encode(str.encode(string))
    return string


def decode_word(string):
    string = base64.b64decode(string)
    string = string.decode('utf-8')
    return string
