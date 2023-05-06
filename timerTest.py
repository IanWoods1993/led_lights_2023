import time
import getch
import threading

threadList = []

def hell():
    global threadList
    print("hell")
    threadList.pop()


i = 0
while True:
    print(i)
    if len(threadList) == 0:
        print("Adding one to the list")
        t = threading.Timer(5, hell)
        threadList.append(t)
        t.start()

    time.sleep(1)

    i = i + 1
