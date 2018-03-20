#!/usr/bin/env python

import sys

dictionaryPath = "./dictionary.txt"
categoryList = []

def isEntryLine(line):
    return (line.find("): ") >= 0)

def isCategoryLine(line):
    return (line.find("> ") == 0)

def getLineCategoryName(line):
    endIndex = line.find("(")
    if endIndex < 0:
        endIndex = len(line)
    return line[2:endIndex]

def getLineCategorySyllable(line):
    index = line.find("(")
    if index < 0:
        return None
    return line[(index + 1):(index + 3)].upper()

def leftPad(text, length):
    while len(text) < length:
        text = " " + text
    return text

class Entry(object):
    
    def __init__(self, line):
        index = line.find("(");
        if index > 0:
            self.word = line[0:(index - 1)].upper()
        else:
            self.word = None
        tempEndIndex = line.find("): ")
        self.partOfSpeech = line[(index + 1):tempEndIndex]
        index = self.partOfSpeech.find("*")
        if index >= 0:
            self.partOfSpeech = self.partOfSpeech[0:index]
            self.hasAntonym = True
        else:
            self.hasAntonym = False
        self.definition = line[(tempEndIndex + 3):len(line)]

class Category(object):
    
    def __init__(self, line):
        self.name = getLineCategoryName(line)
        self.syllable = getLineCategorySyllable(line)
        self.entryList = []
    
    def addEntry(self, entry):
        self.entryList.append(entry)

def compareCategoriesByEntryCount(category1, category2):
    tempCount1 = len(category1.entryList)
    tempCount2 = len(category2.entryList)
    if tempCount1 > tempCount2:
        return -1
    if tempCount1 < tempCount2:
        return 1
    return 0

def readDictionaryFile():
    with open(dictionaryPath, "r") as file:
        inputText = file.read()
    tempList = inputText.split("\n")
    tempLastCategory = None
    for line in tempList:
        if isCategoryLine(line):
            tempCategory = Category(line)
            categoryList.append(tempCategory)
            tempLastCategory = tempCategory
        if isEntryLine(line):
            tempEntry = Entry(line)
            tempLastCategory.addEntry(tempEntry)

def countEntriesCommand():
    readDictionaryFile()
    categoryList.sort(compareCategoriesByEntryCount)
    tempTotal = 0
    for category in categoryList:
        tempName = category.name
        tempCount = len(category.entryList)
        tempText = tempName + ": " + str(tempCount)
        tempText2 = "*" * tempCount
        while len(tempText2) < 50:
            if len(tempText2) % 2 == 1:
                tempText2 += "|"
            else:
                tempText2 += " "
        print leftPad(tempText, 35) + " " + tempText2
        tempTotal += tempCount
    print "Total word count: " + str(tempTotal)
    print "Number of categories: " + str(len(categoryList))

def printCliUsageAndQuit():
    print "Usage:"
    print "./entryDigest.py countEntries"
    sys.exit(0)

print "Entry Digest"

if len(sys.argv) < 2:
    printCliUsageAndQuit()

commandName = sys.argv[1]

if commandName == "countEntries":
    countEntriesCommand()
else:
    printCliUsageAndQuit()

print "Finished."


