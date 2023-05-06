# Parallel code with shared variables, using threads
from threading import Lock, Thread
from time import sleep
import getch

# Variables to be shared across threads
counter = 0
run = True
lock = Lock()

# Function to be executed in parallel
def myfunc():

    # Declare shared variables
    global run
    global counter
    global lock

    # Processing to be done until told to exit
    while run:
        sleep( 1 )

        # Increment the counter
        lock.acquire()
        counter = counter + 1
        lock.release()

    # Set the counter to show that we exited
    lock.acquire()
    counter = -1
    lock.release()
    print( 'thread exit' )

# ----------------------------

# Launch the parallel function as a thread
thread = Thread(target=myfunc)
thread.start()

# Read and print the counter
while counter < 5:
    print( counter )
    sleep( 1 )

# Change the counter    
lock.acquire()
counter = 0
lock.release()

# Read and print the counter
while counter < 5:
    print( counter )
    sleep( 1 )
    
# Tell the thread to exit and wait for it to exit
run = False
thread.join()

# Confirm that the thread set the counter on exit
print( counter )
