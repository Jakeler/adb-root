# adb root
This script allows to push/pull files as root over adb (rooted Android device with working busybox/toybox required).
```
usage: adb-root.py [-h] [-m MODE] [-o OWNER] [-c] [--verbose]
                   [--verbosity {DEBUG,INFO,WARNING,ERROR}]
                   {push,pull} source target

read/write files as root on any Android device

positional arguments:
  {push,pull}                             pull to copy from device, push to copy to device
  source                                  path of the file to copy
  target                                  destination for the copied file

optional arguments:
  -h, --help                              show this help message and exit
  -m MODE, --mode MODE                    set mode of file (chmod notation)
  -o OWNER, --owner OWNER                 set owner and group of file (chown notation)
  -c, --check                             calculate and compare hashsum after transfer
  --verbose, -v                           Increase verbosity from default warning level
  --verbosity {DEBUG,INFO,WARNING,ERROR}  Directly set logging level
```

### Technical background
(TODO: blog post)

It reads the file to stdout, sends the stream over adb to a root shell, which writes it with dd to disk/flash. 
Changing mode/owner and is done with directly calling chmod/chown and the hashsum check with sha256.

Recursive handling of directories is currently not implemented, but planned for the future.

### Speed
In my tests comparable to the normal adb push/pull, about USB 2.0 performance (30 MB/s). Small files can be drastically slower, because of the shell spawning overhead.
