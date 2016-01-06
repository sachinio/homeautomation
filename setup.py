
# This script should be run if switching devices
# It will setup all the prerequisites for this project.

import subprocess

apt_packages = ['git', 'python-pip', 'mongodb']
pip_packages = ['flask', 'pymongo', 'webpigpio']


def run_process(cmd):
    p = subprocess.Popen(cmd)
    p.communicate()


def install_apt_packages():
    cmd = ['sudo', 'apt-get', 'install', '-y']
    cmd.extend(apt_packages)
    run_process(cmd)


def install_pip_packages():
    for pack in pip_packages:
        cmd = ['sudo', 'pip', 'install', pack, '--upgrade']
        run_process(cmd)

run_process(['sudo', 'apt-get', 'update'])
install_apt_packages()
install_pip_packages()

print('Yay! Your new PI is ready.')