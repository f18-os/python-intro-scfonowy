# CS4375 - Python Shell Assignment
--
*by super anonymous student, last update September 19th, 2018*
## Overview
This project contains a simple shell implemented in Python. Thus far, it is able to execute programs and pass arguments, and handle file redirection via the '>' and '<' operators. The shell is also capable of handling a single pipe between two commands with no added redirection. Finally, the shell can change directories using "cd" and commands ended with a "&" character are processed in the background.

There is a wordcount script included under the 'wordcount' directory with its own assignment prompt and README.

## Running Instructions
To run the script, simply download or clone the repository and run the shell.py script using `python3`. For example:

`python3 shell/shell.py` or `./shell/shell.py`

## References
Code for reading and checking command line arguments was sampled from demo files provided by the instructor, Dr. Freudenthal.

The Python 3 documentation describing regexes in Python was referenced for splitting strings (https://docs.python.org/3/howto/regex.html).

The Python 3 documentation describing OS interfaces in Python was referenced for pipes, dup2, environ, etc. (https://docs.python.org/2/library/os.html).

I also found this TutorialsPoint article on pipes useful (https://www.tutorialspoint.com/python/os_pipe.htm).