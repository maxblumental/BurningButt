import threading as th
import pexpect as pe

class HackerThread(th.Thread):

    def __init__(self, remainder, np, event, filename):
        super(HackerThread, self).__init__()
        self._remainder = remainder
        self._np = np
        self._event = event
        self._filename = filename

    def run(self):
       
        effort = self._remainder

        while 1:

            if self._event.isSet():
                quit()
        
            child = pe.spawn('unzip '+self._filename)

            try:
                child.expect('password:', timeout=2)
            except pe.ExceptionPexpect as ex:
                #print ex.message
                print "Didn't get password prompt!"
                self._event.set()
                quit()

            child.sendline(str(effort))

            try:
                child.expect('reenter:', timeout=2)
            except pe.ExceptionPexpect as ex:
                #print ex.message
                print "Success!"
                self._event.set()
                quit()

            effort += self._np


if __name__ == '__main__':

    #np = int(raw_input('Number of threads:'))
    np = 4
    filename = "secure.zip"

    event = th.Event()

    threads = [ HackerThread(i, np, event, filename) for i in range(np) ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join(timeout=None)
