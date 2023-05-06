import threading
import getch
import time

shouldStartNewThread = True

def getInput():
    global shouldStartNewThread
    userInput = getch.getch()
    print(userInput)
    shouldStartNewThread = True


#inputThread = inputThread.start()

while True:
    inputThread = threading.Thread(target=getch.getch)
    inputThread.start()
    print("Thingie")
    inputThread.join(timeout = 1)
    time.sleep(1)

