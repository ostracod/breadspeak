#!/usr/bin/env python

import sys

dictionaryPath = "./dictionary.txt"
categoryList = []

def isDictionaryLine(line):
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

class Category(object):
    def __init__(self, line):
        self.name = getLineCategoryName(line)
        self.syllable = getLineCategorySyllable(line)
        self.count = 0

def compareCategoriesByEntryCount(category1, category2):
    if category1.count > category2.count:
        return -1
    if category1.count < category2.count:
        return 1
    return 0

def readDictionaryFile():
    with open(dictionaryPath, "r") as file:
        inputText = file.read()
    tempList = inputText.split("\n")
    index = 0
    while index < len(tempList):
        tempLine = tempList[index]
        if isCategoryLine(tempLine):
            tempCategory = Category(tempLine)
            categoryList.append(tempCategory)
        if isDictionaryLine(tempLine):
            tempCategory = categoryList[len(categoryList) - 1]
            tempCategory.count += 1
        index += 1

def countWordsCommand():
    readDictionaryFile()
    categoryList.sort(compareCategoriesByEntryCount)
    tempTotal = 0
    for category in categoryList:
        tempName = category.name
        tempCount = category.count
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
    print "./entryDigest.py countWords"
    sys.exit(0)

print "Entry Digest"

if len(sys.argv) < 2:
    printCliUsageAndQuit()

commandName = sys.argv[1]

if commandName == "countWords":
    countWordsCommand()
else:
    printCliUsageAndQuit()

print "Finished."


