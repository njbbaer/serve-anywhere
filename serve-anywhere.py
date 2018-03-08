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


def setup_tunnel():
    ssh_command = 'ssh -i %s -NR %s:localhost:%s %s@%s' % (\
        KEY_FILE, PUBLIC_PORT, LOCAL_PORT, USERNAME, ADDRESS)
    tunnel_process = subprocess.Popen(ssh_command, stderr=subprocess.PIPE, shell=True)

    print('Establishing connection to gateway...')

    read_ouput_process = multiprocessing.Process(target=read_output, name="read_output", args=(tunnel_process,))
    read_ouput_process.start()

    established = False
    start_time = time.time()
    while read_ouput_process.is_alive():
        if time.time() > start_time + 5 and not established:
            print("Done. Available at http://%s:%s" % (ADDRESS, PUBLIC_PORT))
            established = True

    @atexit.register
    def cleanup():
        tunnel_process.kill()
        read_ouput_process.terminate()


def read_output(process):
    output = process.stderr.readline()
    print(output.rstrip().decode("utf-8"))
    sys.exit(0)


if __name__ == '__main__':
    setup_tunnel()