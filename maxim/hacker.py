import itertools
import threading as th
import pexpect as pe

class HackerThread(th.Thread):

    def __init__(self, i, index, np, event, archive_name, length, key):
        super(HackerThread, self).__init__()
        self._i = i
        self._index = index
        self._np = np
        self._event = event
        self._archive_name = archive_name
        self._filename = ''
        self._length = length
        self._key = key
        self._itertable = 'abcdefjhiklmnoprqrstvxyzABCDEFGHIKLMNOPQRSTVXYZ1234567890!@#%^&*_=+()'
            

    def communicator(self, plst):

            password = plst[self._i]

            print('COMM: '+password)

            if self._event.isSet():
                quit()
        
            child = pe.spawn('gpg -o file -d '+self._archive_name)

            try: 
                child.expect('passphrase:', timeout=2)
            except pe.ExceptionPexpect as ex:
                #print ex.message
                print "Didn't get password prompt!"
                self._event.set()
                quit()

            #feed the password to unzip
            child.sendline(str(password))

            try:
                child.expect('bad key', timeout=2)
            except pe.ExceptionPexpect as ex:
                print 'HERE I AM '+str(password)
                print ex.message
                print "Success!"
                self._event.set()
                child.kill(0)
                return True

            child.kill(0)
            return False

    def check(self, result): 
        if result != '':
            self._event.set()
            print(result)
            quit()

    def run(self):

        result = ""

        #result = self.break_fool()
        #print(result)
        #self.check(result)
        if self._key == '' and self._length == 0:
            result = self.brute_force()
            self.check(result)
        if self._length != 0 and self._key == '':
            result = self.brute_force_length()
            self.check(result)
        if self._key != '' and self._length == 0:
            result = self.brute_force_hint()
            self.check(result)
        if self._key != '' and self._length != 0:
            result = self.brute_force_hint_length()
            self.check(result)
        quit()

    def break_fool(self): 
            if self._length != 0:
                self._filename = "./fool_tables/full_Fool_table_" + str(self._length) + ".txt"
            else:
                self._filename = "./fool_tables/full_Fool_table.txt"
            fFt = open(self._filename,'r')
            plst = []
            for line in fFt:
                plst.append(line)
                if len(plst) == self._np:
                    if self.communicator(plst):
                        return plst[self._i]
                    plst = []
            return ""

    def helper(self, length):
           password = ''
           plst = []
           for i in itertools.combinations_with_replacement(self._itertable, length):
                 for k in range(length):
                       password += i[k]
                 plst.append(password)
                 if len(plst) == self._np:
                    if self.communicator(plst):
                       return plst[self._i]
                    plst = []
                 password = ''
           return ""

    def brute_force(self):
          for j in range (1, 16):
            password = self.helper(j)
          print(password)
          if (password != ""):
              return password
          return ""

    def brute_force_length(self):                  
          password = self.helper(self._length)
          if (password != ""):
              return password
          return ""

    def helper_hint(self, length):
                    password = ''
                    parts = []
                    plst = []
                    for i in itertools.combinations_with_replacement(self._itertable, length):
                        for k in range(length):
                            parts.append(i[k])
                        parts.append(self._key)
                        for k in itertools.permutations(parts):
                            for m in range(length + 1):
                                password += k[m]
                            plst.append(password)
                            if len(plst) == self._np:
                               if self.communicator(plst):
                                   return plst[self._i]
                               plst = []
                            password = ''
                        parts = []
                    return ""

    def brute_force_hint(self):
            for j in range (1, 16):
                password = self.helper_hint(j)
                if (password != ""):
                   return password
            return ""

    def brute_force_hint_length(self):
            password = self.helper_hint(self._length - len(self._key))
            if (password != ""):
                return password
            return ""


if __name__ == '__main__':

    #User input
    np = 4
    index = 0
    length = 0
    key = 'ab'
    filename = "secure.gpg"
    #Hint to be added

    event = th.Event()

    threads = [ HackerThread(i, index, np, event, filename, length, key) for i in range(np) ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join(timeout=None)
