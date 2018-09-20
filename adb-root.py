#!/bin/env python
import argparse, subprocess, logging

parser = argparse.ArgumentParser(description="read/write files as root on any Android device")
parser.add_argument("action", choices=["push", "pull"], help="pull to copy from device, push to copy to device")
parser.add_argument("source", help="path of the file to copy")
parser.add_argument("target", help="destination for the copied file")
parser.add_argument("-m", "--mode", help="set mode of file (chmod notation)")
parser.add_argument("-o", "--owner", help="set owner and group of file (chown notation)")
parser.add_argument("-c", "--check", help="calculate and compare hashsum after transfer",  action="store_true")
parser.add_argument('--verbose', '-v', action='count', help="Increase verbosity from default warning level")
parser.add_argument('--verbosity', choices=["DEBUG", "INFO", "WARNING", "ERROR"], help="Directly set logging level")
args = parser.parse_args()


loglevel = args.verbosity if args.verbosity else 30
if args.verbose:
    loglevel -= args.verbose*10
    
logging.basicConfig(format='[%(relativeCreated)d ms] %(levelname)s:%(message)s', level=loglevel)


def log_exitcode(action, result):    
    code = result.returncode
    if code == 0:
        logging.info("%s on %s successful", action, args.target)
    else:
        logging.error("Error, exitcode: %d", code)
    logging.debug(result)
    
def hash_check(local, remote):
        logging.info("Started integrity check with SHA256")
        hash_src = subprocess.run(["sha256sum", local], stdout=subprocess.PIPE).stdout.decode('utf-8')[:64]
        hash_dest = subprocess.run(['adb', 'shell', "su -c", "sha256sum", remote], stdout=subprocess.PIPE).stdout.decode('utf-8')[:64]
        if hash_src == hash_dest:
            logging.info("Integrity ok: %s => %s (%s)" % (local, remote, hash_src))
        else:
            logging.error("Check failed, hashsum mismatch: %s vs %s" % (hash_src, hash_dest))

def push():
    logging.info("Started pushing %s", args.source)
    with open(args.source, "r") as file:
        result = subprocess.run(['adb', 'shell', 'su -c', 'dd of=/'+args.target], stdin=file)
        log_exitcode("Transfer", result)

    if args.mode:
        result = subprocess.run(['adb', 'shell', 'su -c', 'chmod', args.mode, args.target])
        log_exitcode("Change mode", result)
    if args.owner:
        result = subprocess.run(['adb', 'shell', 'su -c', 'chown', args.owner, args.target])
        log_exitcode("Change owner", result)
    
    if args.check:
        hash_check(args.source, args.target)


def pull():
    logging.info("Started pulling %s", args.source)
    with open(args.target, "w+") as file:
        result = subprocess.run(['adb', 'shell', "su -c", "dd if="+args.source], stdout=file)
        log_exitcode("Transfer", result)
        
    if args.check:
        hash_check(args.target, args.source)
            
    if args.mode or args.owner:
        logging.warning("mode/owner ignored for pull!")

if args.action == "push":
    push()
elif args.action == "pull":
    pull()
