# CS4375 - Intro to Python Assignment
--
*Steven Brooks, last update September 3rd, 2018*
## Overview
This short Python 3 script reads in an input text (.txt) file and outputs a text (.txt) file that contains all words in the input text, sorted, along with the number of occurrences of each word. Note that words are delimited by any non-alphanumeric character, i.e. "it's" will be counted as "it" and "s". This conforms to the test cases provided by the instructor.

## Running Instructions
To run the script, simply download or clone the repository and run the wordCount.py script using `python3`. For example:

`python3 wordCount.py exampleInput.txt exampleOutput.txt`

Note that the program will overwrite the passed output file if it already exists.

## Original Assignment Prompt
The original prompt for this assignment can be found in AssignmentPrompt.md.

## References
Code for reading and checking command line arguments was sampled from the wordCountTest.py file provided with the assignment. The Python 3 documentation describing regexes in Python was referenced for splitting strings (https://docs.python.org/3/howto/regex.html). List functions (filter, sorted) and list comprehensions have been picked up over a variety of past course assignments using Python.
