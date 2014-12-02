import pexpect as pe

presumable_passwords = ['cat','hello']

child_process = pe.spawn('unzip secure.zip')
child_process.expect('password:')

for ppswd in presumable_passwords:
    child_process.sendline(ppswd)
    try:
        child_process.expect('reenter:', timeout=2)
    except:
        print "Success!"
        quit()

print "Fail!"
