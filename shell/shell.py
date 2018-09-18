#! /usr/bin/env python3

import os, sys, re, signal

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

'''
Function that creates child processes and pipes I/O of input commands.
param args : A list of string arguments read from the shell.
'''
def pipe(args):
    inPipe, outPipe = os.pipe()

    fork_code = os.fork()

    if fork_code == 0: # in child
        args = args[args.index("|") + 1:]
        os.close(outPipe)

        sys.stdin = os.fdopen(inPipe, "r")
        os.dup2(sys.stdin.fileno(), 0)
        os.set_inheritable(sys.stdin.fileno(), True)
        execute(args)
    
    elif fork_code > 0: # in parent
        fork_code = os.fork()

        if fork_code == 0: # in child, again
            args = args[:args.index("|")]
            os.close(inPipe)

            sys.stdout = os.fdopen(outPipe, "w")
            os.dup2(sys.stdout.fileno(), 1)
            os.set_inheritable(sys.stdout.fileno(), True)
            execute(args)
            
        elif fork_code > 0: # in parent, again
            os.close(outPipe) # close pipe FDs
            os.close(inPipe)
            sys.exit(0) # close this process

'''
Function that executes the passed array of input arguments.
param args : A list of string arguments read from the shell.
'''
def execute(args):
    if len(args) > 0:
        for dir in directories: # try each directory in PATH and current working directory
            program = "%s/%s" % (dir, args[0])
            if os.path.exists(program):
                os.execve(program, args, os.environ)

### main
while True:
    # check for PS1 variable in environment
    prompt = ("%s$ " % (os.getcwd())) if ("PS1" not in os.environ) else os.environ["PS1"]

    try:
        sys.stdin.flush() # flush I/O buffers (resolves some issues with piping)
        sys.stdout.flush()

        args = str(input(prompt)).split() # get user input and split on spaces
        fork_code = os.fork()

        if fork_code == 0: # in child
            directories = re.split(":", os.environ['PATH'])
            directories.append(os.getcwd())
            directories.append("")

            if ("<" in args or ">" in args) and "|" in args:
                os.write(2, "ERROR: Unable to process both pipe and redirect.")
                continue
            elif ("<" in args or ">" in args):
                redirect(args) # handle any redirections
                execute(args)
            elif "|" in args:
                pipe(args) # handle pipes
            else:
                execute(args) # just execute command w/ args

        elif fork_code > 0: # in parent, wait for child process
            os.wait()

        else: # error
            os.write(2, "ERROR: Unable to fork.\n".encode())
            sys.exit(1)
    except EOFError:
        exit()
