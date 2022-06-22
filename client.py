import socket
import pickle


def get_notices():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.0.102',9876))
    s.send(bytes('NOTICE','utf-8'))

    msg = s.recv(10000)
    data = pickle.loads(msg)
    return data

def get_homework():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.0.102',9876))
    s.send(bytes('HOMEWORK','utf-8'))

    msg = s.recv(10000)
    data = pickle.loads(msg)
    return data