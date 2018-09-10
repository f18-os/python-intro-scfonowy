#! /usr/bin/env python3

import os, sys, re

pid = os.getpid() # store shell's pid

while True:
    args = str(input("%s$" % (os.getcwd()))).split() # get user input and split on spaces

    fork_code = os.fork()

    if fork_code == 0: # in child
        directories = re.split(":", os.environ['PATH'])
        directories.append(os.getcwd())

        for dir in directories: # try each directory in PATH and current working directory
            program = "%s/%s" % (dir, args[0])
            if os.path.exists(program):
                os.execve(program, args, os.environ)

    elif fork_code > 0: # in parent, wait for child process
        os.wait()

    else: # error
        os.write(2, "ERROR: Unable to fork.\n".encode())
        sys.exit(1)
