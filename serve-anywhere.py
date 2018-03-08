import subprocess
import multiprocessing
import atexit
import time
import sys


ADDRESS = '184.72.16.74'
USERNAME = 'serve-anywhere'
KEY_FILE = 'auth_key'
LOCAL_PORT = 3000
PUBLIC_PORT = 50000
 
ssh_command = 'ssh -i %s -NR %s:localhost:%s %s@%s' % (\
    KEY_FILE, PUBLIC_PORT, LOCAL_PORT, USERNAME, ADDRESS)
process = subprocess.Popen(ssh_command, stdout=subprocess.PIPE, shell=True)

print('Establishing tunnel...', end='', flush=True)
print('done')
print('http://%s:%s' % (ADDRESS, PUBLIC_PORT))

while True:
    pass

@atexit.register
def cleanup():
    process.kill()