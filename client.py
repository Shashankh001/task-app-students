import socket
import pickle

def get_ip():
    with open('ip.txt') as f:
        return f.read()

IP = get_ip()

def get_notices():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP,9876))
    s.send(bytes('NOTICE','utf-8'))

    msg = s.recv(10000)
    data = pickle.loads(msg)
    return data

def get_homework():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP,9876))
    s.send(bytes('HOMEWORK','utf-8'))

    msg = s.recv(10000)
    data = pickle.loads(msg)
    return data