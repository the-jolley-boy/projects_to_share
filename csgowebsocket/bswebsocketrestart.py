import subprocess as sp
import time

while True:
    extproc = sp.Popen(['python', 'bswebsocket.py'])

    time.sleep(300)

    sp.Popen.terminate(extProc)
