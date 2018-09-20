#! /usr/bin/env python3

import os, sys, re

def redirect(args):
    """
    Function that handles redirection arguments in an array of input arguments. This function removes the redirection symbols and the source/destination of the redirections.

    Arguments:
    args -- A list of string arguments that includes at least one I/O redirection.
    """
    if ">" in args:
        filename = args[args.index(">") + 1] # get filename

        sys.stdout = open(filename, "w+") # set standard output
        os.dup2(sys.stdout.fileno(), 1) # dup2 closes stdout and copies new output FD
        os.set_inheritable(sys.stdout.fileno(), True)

        args.pop(args.index(">") + 1) # remove redirection
        args.pop(args.index(">"))

    if "<" in args:
        filename = args[args.index("<") + 1] # get filename

        sys.stdin = open(filename, "r") # set standard input
        os.dup2(sys.stdin.fileno(), 0) # dup2 closes stdin and copies new input FD
        os.set_inheritable(sys.stdin.fileno(), True)

        args.pop(args.index("<") + 1) # remove redirection
        args.pop(args.index("<"))


def pipe(args):
    """
    Function that creates child processes and pipes I/O of input commands.

    Arguments:
    args -- A list of string arguments, split by a single pipe.
    """
    inPipe, outPipe = os.pipe()

    fork_code = os.fork() # fork off for receiving process

    if fork_code == 0: # in child, configure receiving program
        args = args[args.index("|") + 1:]
        os.close(outPipe) # close unused out FD

        sys.stdin = os.fdopen(inPipe, "r")
        os.dup2(sys.stdin.fileno(), 0) # need to dup over stdin 0
        os.set_inheritable(sys.stdin.fileno(), True)
        execute(args)
    
    elif fork_code > 0: # in parent, fork off again for output process
        fork_code = os.fork()

        if fork_code == 0: # in child, configure output program
            args = args[:args.index("|")]
            os.close(inPipe) # close unused in FD

            sys.stdout = os.fdopen(outPipe, "w")
            os.dup2(sys.stdout.fileno(), 1) # need to dup over stdout 1
            os.set_inheritable(sys.stdout.fileno(), True)
            execute(args)
            
        elif fork_code > 0: # in parent process
            os.close(outPipe) # close both pipe FDs
            os.close(inPipe)

            sys.exit(0) # close this process (only used to create the child processes)
    else: # unable to fork
        os.write(2, "ERROR: Unable to fork.\n".encode())


def execute(args):
    """
    Function that executes the passed array of input arguments, passing the first argument to execve.

    Arguments:
    args -- A list of string arguments, the first of which is the program to run.
    """
    if len(args) > 0:
        for dir in directories: # try each directory in PATH and current working directory
            program = "%s/%s" % (dir, args[0])
            if os.path.exists(program):
                os.execve(program, args, os.environ)
    else: # no commands to execute, terminate
        sys.exit(0)

### main
while True:
    # check for PS1 variable in environment and set prompt statement accordingly
    prompt = ("%s$ " % (os.getcwd())) if "PS1" not in os.environ else os.environ["PS1"]

    try:
        sys.stdin.flush() # flush I/O buffers (resolves some issues with piping)
        sys.stdout.flush()

        args = str(input(prompt)).split() # get user input and split on spaces

        if "cd" in args: # handle directory change
            try:
                os.chdir(args[args.index("cd") + 1])
            except:
                os.write(2, "ERROR: Unable to change directories.")
            continue # no command to execute, skip rest of loop
        
        background = "&" in args # check if command should run in background
        if background:
            args.pop(args.index("&"))
        
        fork_code = os.fork() # create process to handle program execution

        if fork_code == 0: # in child
            directories = re.split(":", os.environ['PATH']) # get all directories in PATH
            directories.append(os.getcwd()) # add the current working directory
            directories.append("") # add root directory (for full name programs)

            if ("<" in args or ">" in args) and "|" in args: # error case: i'm not smart enough for both at once, sorry
                os.write(2, "ERROR: Unable to process both pipe and redirect, sorry.")
                sys.exit(0) # terminate this process
            elif ("<" in args or ">" in args):
                redirect(args) # handle any redirections before executing
                execute(args)
            elif "|" in args:
                pipe(args) # handle pipes
            else:
                execute(args) # just execute command w/ args

        elif fork_code > 0: # in parent, wait for child process to finish
            if not background:
                os.wait()

        else: # error case
            os.write(2, "ERROR: Unable to fork.\n".encode())
            sys.exit(1)
    except EOFError: # shell terminates on EOF character (CTRL-D)
        exit()
