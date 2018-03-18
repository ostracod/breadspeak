#!/usr/bin/env python

import sys

def isDictionaryLine(line):
    return line.find("): ") >= 0

def getLineCategoryName(line):
    if line.find("> ") == 0:
        return line[2:len(line)]
    else:
        return None

def leftPad(text, length):
    while len(text) < length:
        text = " " + text
    return text

class Category(object):
    def __init__(self, name):
        self.name = name
        self.count = 0

def compareCategories(category1, category2):
    if category1.count > category2.count:
        return -1
    if category1.count < category2.count:
        return 1
    return 0

def processInputFile():
    tempCategoryList = []
    tempFile = open(inputFileName, "r")
    inputText = tempFile.read()
    tempFile.close()
    tempList = inputText.split("\n")
    index = 0
    while index < len(tempList):
        tempLine = tempList[index]
        tempCategoryName = getLineCategoryName(tempLine)
        if tempCategoryName is not None:
            tempCategory = Category(tempCategoryName)
            tempCategoryList.append(tempCategory)
        if isDictionaryLine(tempLine):
            tempCategory = tempCategoryList[len(tempCategoryList) - 1]
            tempCategory.count += 1
        index += 1
    tempCategoryList.sort(compareCategories)
    tempTotal = 0
    index = 0
    while index < len(tempCategoryList):
        tempCategory = tempCategoryList[index]
        tempName = tempCategory.name
        tempCount = tempCategory.count
        tempText = tempName + ": " + str(tempCount)
        tempText2 = "*" * tempCount
        while len(tempText2) < 50:
            if len(tempText2) % 2 == 1:
                tempText2 += "|"
            else:
                tempText2 += " "
        print leftPad(tempText, 35) + " " + tempText2
        tempTotal += tempCount
        index += 1
    print "Total word count: " + str(tempTotal)
    print "Number of categories: " + str(len(tempCategoryList))

print "Word Counter"

if len(sys.argv) < 2:
    print "Please provide one file name as an argument."
    sys.exit(0)

inputFileName = sys.argv[1];

processInputFile()

print "Finished."

