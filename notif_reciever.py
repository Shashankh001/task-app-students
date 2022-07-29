import socket
from threading import Thread
import time
from win10toast import ToastNotifier

toaster = ToastNotifier()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0',2231))
s.listen(100)


def thread(cs):
    arg = cs.recv(1024)
    arg = arg.decode("utf-8")

    time.sleep(1.5)
    message = cs.recv(1024)
    message = message.decode("utf-8")

    if arg == 'HW':
        toaster.show_toast('Homework recieved!',message)

    if arg == 'NOT':
        toaster.show_toast('Notice recieved!',message)



while True:
    cs, address = s.accept()

    t = Thread(target = thread, args = (cs,))
    t.daemon = True
    t.start()

    print(f"{address} has sent a notification.")