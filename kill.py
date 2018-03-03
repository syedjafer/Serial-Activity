#!/usr/bin/env python
import sys
from multiprocessing.pool import ThreadPool

import paramiko

BASE_ADDRESS = "192.168.7."
USERNAME = "t1"
PASSWORD = "uni1"


def create_client(hostname):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname, username=USERNAME, password=PASSWORD)
    ssh_client.invoke_shell()
    return ssh_client


def kill_computer(ssh_client):
    """Power off a computer."""
    ssh_client.exec_command("poweroff")


def install_python_modules(ssh_client):
    """Install the programs specified in requirements.txt"""
    ftp_client = ssh_client.open_sftp()

    # Move over get-pip.py
    local_getpip = "/home/jafer/lab_freak/get-pip.py"
    remote_getpip = "/home/%s/Documents/get-pip.py" % USERNAME
    ftp_client.put(local_getpip, remote_getpip)

    # Move over requirements.txt
    local_requirements = "/home/jafer/lab_freak/requirements.txt"
    remote_requirements = "/home/%s/Documents/requirements.txt" % USERNAME
    ftp_client.put(local_requirements, remote_requirements)

    ftp_client.close()

    # Install pip and the desired modules.
    ssh_client.exec_command("python %s --user" % remote_getpip)
    ssh_client.exec_command("python -m pip install --user -r %s" % remote_requirements)


def worker(action, hostname):
    ssh_client = create_client(hostname)

    if action == "kill":
        kill_computer(ssh_client)
    elif action == "install":
        install_python_modules(ssh_client)
    else:
        raise ValueError("Unknown action %r" % action)


def main():
    if len(sys.argv) < 2:
        print("USAGE: python kill.py ACTION")
        sys.exit(1)

    hostnames = [str(BASE_ADDRESS) + str(i) for i in range(30, 60)]

    with ThreadPool() as pool:
        pool.map(kill_computer, hostnames)


if __name__ == "__main__":
    main()
