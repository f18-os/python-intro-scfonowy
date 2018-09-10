#! /usr/bin/env python3

import os, sys, re

pid = os.getpid() # store shell's pid

'''
Function that handles redirection arguments in an array of input arguments.
param args : A list of string arguments read from the shell.
'''
def redirect(args):
    if ">" in args:
        os.close(1) # close standard out
        filename = args[args.index(">") + 1] # get filename

        sys.stdout = open(filename, "w+") # set standard output
        os.set_inheritable(sys.stdout.fileno(), True)

        args.pop(args.index(">") + 1) # remove redirection
        args.pop(args.index(">"))

    if "<" in args:
        os.close(0) # close standard in
        filename = args[args.index("<") + 1] # get filename

        sys.stdin = open(filename, "r") # set standard input
        os.set_inheritable(sys.stdin.fileno(), True)

        args.pop(args.index("<") + 1) # remove redirection
        args.pop(args.index("<"))


### main
while True:
    args = str(input("%s$ " % (os.getcwd()))).split() # get user input and split on spaces

    fork_code = os.fork()

    if fork_code == 0: # in child
        directories = re.split(":", os.environ['PATH'])
        directories.append(os.getcwd())

        redirect(args) # handle any redirections

        for dir in directories: # try each directory in PATH and current working directory
            program = "%s/%s" % (dir, args[0])
            if os.path.exists(program):
                os.execve(program, args, os.environ)

    elif fork_code > 0: # in parent, wait for child process
        os.wait()

    else: # error
        os.write(2, "ERROR: Unable to fork.\n".encode())
        sys.exit(1)
