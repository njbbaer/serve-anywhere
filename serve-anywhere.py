import subprocess
import multiprocessing
import atexit
import time
import sys

from config import config

def setup_tunnel(address, username, key_file, local_port, public_port):
    ssh_command = "ssh -i %s -NR %s:localhost:%s %s@%s" % (\
        key_file, public_port, local_port, username, address)
    tunnel_process = subprocess.Popen(ssh_command, stderr=subprocess.PIPE, shell=True)

    print("Establishing connection to gateway...")

    read_ouput_process = multiprocessing.Process(target=read_output, name="read_output", args=(tunnel_process,))
    read_ouput_process.start()

    established = False
    start_time = time.time()
    while read_ouput_process.is_alive():
        if time.time() > start_time + 3 and not established:
            print("Done. Available at http://%s:%s" % (address, public_port))
            established = True

    @atexit.register
    def cleanup():
        tunnel_process.kill()
        read_ouput_process.terminate()


def read_output(process):
    output = process.stderr.readline()
    print(output.rstrip().decode("utf-8"))
    sys.exit(0)


if __name__ == "__main__":
    setup_tunnel(
        config["gateway_address"],
        config["username"],
        config["key_file"],
        3000, 50000)