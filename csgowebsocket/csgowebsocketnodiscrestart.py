import subprocess as sp
import time

while True:
    extProc = sp.Popen(['python','csgowebsocket.py'])

    time.sleep(300)

    sp.Popen.terminate(extProc)
