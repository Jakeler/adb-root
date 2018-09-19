#!/bin/env python
import argparse

parser = argparse.ArgumentParser(description="read/write files as root on any Android device")
parser.add_argument("action", choices=["push", "pull"], help="pull to copy from device, push to copy to device")
parser.add_argument("source", help="path of the file to copy")
parser.add_argument("target", help="destination for the copied file")
parser.add_argument("-m", "--mode", help="set mode of file (chmod notation)")
parser.add_argument("-o", "--owner", help="set owner and group of file (chown notation)")
parser.add_argument("-c", "--check", help="calculate and compare hashsum after transfer",  action="store_true")
args = parser.parse_args()

def push():
    pass
def pull():
    pass

if args.action == "push":
    push()
elif args.action == "pull":
    pull()

