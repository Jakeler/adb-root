#!/bin/env python
import argparse, subprocess

parser = argparse.ArgumentParser(description="read/write files as root on any Android device")
parser.add_argument("action", choices=["push", "pull"], help="pull to copy from device, push to copy to device")
parser.add_argument("source", help="path of the file to copy")
parser.add_argument("target", help="destination for the copied file")
parser.add_argument("-m", "--mode", help="set mode of file (chmod notation)")
parser.add_argument("-o", "--owner", help="set owner and group of file (chown notation)")
parser.add_argument("-c", "--check", help="calculate and compare hashsum after transfer",  action="store_true")
args = parser.parse_args()

def log_exitcode(code):
    if code != 0:
            print("Error, exitcode: %d" % code)

def push():
    with open(args.source, "r") as file:
        result = subprocess.run(['adb', 'shell', 'su -c', 'dd of=/'+args.target], stdin=file)
        log_exitcode(result.returncode)

    if args.mode:
        result = subprocess.run(['adb', 'shell', 'su -c', 'chmod', args.mode, args.target])
        log_exitcode(result.returncode)
    if args.owner:
        result = subprocess.run(['adb', 'shell', 'su -c', 'chown', args.owner, args.target])
        log_exitcode(result.returncode)
    
    if args.check:
        hash_src = subprocess.run(["sha256sum", args.source], stdout=subprocess.PIPE).stdout.decode('utf-8')[:64]
        hash_dest = subprocess.run(['adb', 'shell', "su -c", "sha256sum", args.target], stdout=subprocess.PIPE).stdout.decode('utf-8')[:64]
        if hash_src == hash_dest:
            print("Integrity ok: %s => %s (%s)" % (args.source, args.target, hash_src))
        else:
            print("Check failed, hashsum mismatch: %s vs %s" % (hash_src, hash_dest))


def pull():
    print("Pulling " + args.source)
    with open(args.target, "w+") as file:
        result = subprocess.run(['adb', 'shell', "su -c", "dd if="+args.source], stdout=file)
        log_exitcode(result.returncode)
        
    if args.check:
        hash_src = subprocess.run(['adb', 'shell', "su -c", "sha256sum", args.source], stdout=subprocess.PIPE).stdout.decode('utf-8')[:64]
        hash_dest = subprocess.run(["sha256sum", args.target], stdout=subprocess.PIPE).stdout.decode('utf-8')[:64]
        if hash_src == hash_dest:
            print("Integrity ok: %s => %s (%s)" % (args.source, args.target, hash_src))
        else:
            print("Check failed, hashsum mismatch: %s vs %s" % (hash_src, hash_dest))
            
    if args.mode or args.owner:
        print("Warning: mode/owner ignored for pull!")

if args.action == "push":
    push()
elif args.action == "pull":
    pull()
