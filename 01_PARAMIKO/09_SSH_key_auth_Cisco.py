import sys
import time
import traceback

import paramiko.util # type: ignore
from paramiko import client, ssh_exception, RSAKey # type: ignore  # Add for RSAKey for supported in paramiko private key of key_file path
from getpass import getpass
import socket
#paramiko.util.log_to_file("paramiko.log", level="DEBUG")  #This will create a paramiko logfile you will get some inforamtio to that.it has create once for get a paramiko.log file purpose.

username = 'admin2'
csr_cmd = ['config t', 'int lo1001', 'ip address 1.1.1.1 255.255.255.255', 'end']
key_file = RSAKey.from_private_key_file(filename='/home/vicky/.ssh/id_rsa') # this will mention your exact private key path.
def cisco_cmd_executor(hostname, commands):
    try:
        print(f"Connecting to the device {hostname}..")
        ssh_client = client.SSHClient()
        ssh_client.set_missing_host_key_policy(client.AutoAddPolicy())
        ssh_client.connect(hostname=hostname, port=22, username=username, look_for_keys=True,
                           allow_agent=True,
                           pkey=key_file, # mention key_file int private key file path
                           disabled_algorithms=dict(pubkeys=['rsa-sha2-512', 'rsa-sha2-256'])) # it has must, to support remote ssh of private key authentication.

        print(f"Connected to the device {hostname}")
        device_access = ssh_client.invoke_shell()
        device_access.send("terminal len 0\n")

        for cmd in commands:
            device_access.send(f"{cmd}\n")
            time.sleep(1)
            output = device_access.recv(65535)
            print(output.decode(), end='')

        device_access.send("show run int lo1001\n")
        time.sleep(2)
        output = device_access.recv(65535)
        print(output.decode())
        ssh_client.close()
    except ssh_exception.NoValidConnectionsError:
        print("SSH Port not reachable")
    except socket.gaierror:
        print("Check the hostname")
    except ssh_exception.AuthenticationException:
        print("Authentication failed, check credentials")

    except:
        print("Exception Occurred")
        print(sys.exc_info())
        # traceback.print_exception(*sys.exc_info())

cisco_cmd_executor('192.168.40.10', csr_cmd)

################### important ########################
"""
must you have to create private key for linux then add that pub key to cisco device then you run this script file
"""
