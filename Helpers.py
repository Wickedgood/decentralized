def genkey(password):
    if len(password) < 16:
        while len(password) < 16:
            password = "0"+password
    elif len(password) == 16:
        pass
    else:
        pad = len(password) % 4
        length = (len(password) - pad) + 8
        while len(password) < length:
            password = "0"+password
    return bytes(password,"utf-8")