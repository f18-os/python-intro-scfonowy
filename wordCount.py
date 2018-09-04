#! /usr/bin/env python3

import sys
import re
import os

# check number of arguments
if len(sys.argv) != 3:
    print("Error: Invalid number of arguments. Please refer to the following example:\n\twordCount.py <inputFile>.txt <outputFile>.txt")
    exit()

_, inputFileName, outputFileName = sys.argv # unpack arguments

# check input file exists
if not os.path.exists(inputFileName):
    print ("Error: passed input file does not exist.")
    exit()

wordCountDictionary = {} # mapping of words to counts, i.e. word => count

with open(inputFileName, 'r') as inputFile:
    # read in input file text, split on all non-alphanumeric characters, filter None instances from the result, and convert each item to lowercase
    for word in [w.lower() for w in filter(None, re.split(r'\W', inputFile.read()))]:
        wordCountDictionary[word] = 1 if word not in wordCountDictionary else wordCountDictionary[word] + 1

# write out file w/ word counts
with open(outputFileName, 'w') as outputFile:
    for word, count in sorted(wordCountDictionary.items()):
        outputFile.write(("%s %i\n") % (word, count))