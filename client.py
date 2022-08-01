import socket
import pickle
import sys
import time

def get_ip():
    with open('ip.txt') as f:
        return f.read()

IP = get_ip()

def get_bytesize_string(string, bytelen):
    string_length = sys.getsizeof(string)

    if string_length == bytelen: return None
    
    if string_length < bytelen:
        difference = bytelen - string_length
        for i in range(0, difference):
            string += ' '

        return string

def get_bytesize_bytes(byte, bytelen):
    byte_length = sys.getsizeof(byte)

    if byte_length == bytelen: return None
    
    if byte_length < bytelen:
        difference = bytelen - byte_length
        for i in range(0, difference):
            byte += b' '

        return byte

def get_notices(Class):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP,9876))

    NOTICE = get_bytesize_string('NOTICE',1024)
    s.send(bytes(NOTICE,'utf-8'))

    time.sleep(0.03)

    Class = get_bytesize_string(Class, 1024)
    s.send(bytes(Class,'utf-8'))

    msg = s.recv(10000)
    data = pickle.loads(msg)
    return data

def get_homework(Class):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP,9876))

    HOMEWORK = get_bytesize_string('HOMEWORK',1024)
    s.send(bytes(HOMEWORK,'utf-8'))

    time.sleep(0.03)

    Class = get_bytesize_string(Class, 1024)
    s.send(bytes(Class,'utf-8'))

    msg = s.recv(10000)
    data = pickle.loads(msg)
    return data