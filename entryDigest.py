#!/usr/bin/env python

import sys
from copy import deepcopy

dictionaryPath = "./dictionary.txt"
categorySyllableSet = ["BA", "BE", "DA", "DE", "FA", "FE", "GA", "GE", "KA", "KE", "PA", "PE", "SA", "SE", "TA", "TE", "VA", "VE", "ZA", "ZE"]
consonantSet = ["B", "D", "F", "G", "K", "P", "S", "T", "V", "Z"]
vowelSet = ["A", "E", "I", "O", "U"]
categoryList = []
syllableSet = []

for consonant in consonantSet:
    for vowel in vowelSet:
        syllableSet.append(consonant + vowel)

def isEntryLine(line):
    return (line.find("): ") >= 0)

def isCategoryLine(line):
    return (line.find("> ") == 0)

def getLineCategoryName(line):
    endIndex = line.find(" (")
    if endIndex < 0:
        endIndex = len(line)
    return line[2:(endIndex)]

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
    
    def toString(self):
        if self.word is None:
            output = ""
        else:
            output = self.word.capitalize() + " "
        output += "(" + self.partOfSpeech
        if self.hasAntonym:
            output += "*"
        output += "): " + self.definition
        return output

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

def compareTextCountPair(pair1, pair2):
    tempCount1 = pair1[1]
    tempCount2 = pair2[1]
    if tempCount1 > tempCount2:
        return -1
    if tempCount1 < tempCount2:
        return 1
    return 0

def printBarMetric(text, count, leftPadAmount, maximumCount):
    tempText = text + ": " + str(count)
    tempText2 = "*" * count
    while len(tempText2) < maximumCount:
        if len(tempText2) % 2 == 1:
            tempText2 += "|"
        else:
            tempText2 += " "
    print leftPad(tempText, leftPadAmount) + " " + tempText2

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
    tempWordCount = 0
    for category in categoryList:
        tempName = category.name
        for entry in category.entryList:
            if entry.word is not None:
                tempWordCount += 1
        tempCount = len(category.entryList)
        printBarMetric(tempName, tempCount, 35, 50)
        tempTotal += tempCount
    print "Total entry count: " + str(tempTotal)
    print "Number of entries with words: " + str(tempWordCount)
    print "Number of categories: " + str(len(categoryList))

def categorySyllablesCommand():
    readDictionaryFile()
    tempUnusedSyllableList = deepcopy(categorySyllableSet)
    tempUsedSyllableList = []
    tempDuplicateSyllableList = []
    for category in categoryList:
        tempSyllable = category.syllable
        tempText = leftPad(category.name, 35)
        if tempSyllable is None:
            print tempText + ": No category syllable"
        else:
            print tempText + ": " + tempSyllable + "-"
        if tempSyllable is None:
            continue
        if tempSyllable in tempUnusedSyllableList:
            tempUnusedSyllableList.remove(tempSyllable)
        if tempSyllable in tempUsedSyllableList:
            if tempSyllable not in tempDuplicateSyllableList:
                tempDuplicateSyllableList.append(tempSyllable)
        else:
            tempUsedSyllableList.append(tempSyllable)
    print "Unused category syllables:"
    print tempUnusedSyllableList
    print "Used category syllables:"
    print tempUsedSyllableList
    print "Duplicate category syllables:"
    print tempDuplicateSyllableList

def categoryWordsCommand(syllable):
    readDictionaryFile()
    category = None
    for tempCategory in categoryList:
        if tempCategory.syllable == syllable:
            category = tempCategory
            break
    if category is None:
        print "Could not find category with the syllable " + syllable + "."
        return
    print category.name
    if syllable is None:
        syllable = ""
    tempUnusedWordList = []
    tempUsedWordList = []
    tempDuplicateWordList = []
    for secondSyllable in syllableSet:
        tempUnusedWordList.append(syllable + secondSyllable)
    for entry in category.entryList:
        tempWord = entry.word
        if tempWord is None:
            continue
        if tempWord in tempUnusedWordList:
            tempUnusedWordList.remove(tempWord)
        if tempWord in tempUsedWordList:
            if tempWord not in tempDuplicateWordList:
                tempDuplicateWordList.append(tempWord)
        else:
            tempUsedWordList.append(tempWord)
    tempUnusedWordList.sort()
    tempUsedWordList.sort()
    tempDuplicateWordList.sort()
    print "Unused words:"
    print tempUnusedWordList
    print "Used words:"
    print tempUsedWordList
    print "Duplicate words:"
    print tempDuplicateWordList

def checkForDuplicateWords():
    tempUsedWordList = []
    tempDuplicateWordList = []
    for category in categoryList:
        for entry in category.entryList:
            tempWord = entry.word
            if tempWord is None:
                continue
            if tempWord in tempUsedWordList:
                if tempWord not in tempDuplicateWordList:
                    tempDuplicateWordList.append(tempWord)
            else:
                tempUsedWordList.append(tempWord)
    print "Duplicate words:"
    print tempDuplicateWordList

def duplicateWordsCommand():
    readDictionaryFile()
    checkForDuplicateWords()

def verifyCategorySyllables():
    tempBadWordList = []
    for category in categoryList:
        if category.syllable is None:
            continue
        for entry in category.entryList:
            tempWord = entry.word
            if tempWord is None:
                continue
            tempSyllable = tempWord[0:2]
            if category.syllable != tempSyllable:
                tempBadWordList.append(tempWord)
    print "Words with incorrect syllables:"
    print tempBadWordList

def verifySyllablesCommand():
    readDictionaryFile()
    verifyCategorySyllables()

def wordExistsCommand(word):
    readDictionaryFile()
    for category in categoryList:
        for entry in category.entryList:
            tempWord = entry.word
            if tempWord is not None:
                if tempWord == word:
                    print word + " exists in the dictionary."
                    print entry.toString()
                    return
    print word + " is not in the dictionary."

def verifyAllCommand():
    readDictionaryFile()
    checkForDuplicateWords()
    verifyCategorySyllables()
    tempTotal = 0
    for category in categoryList:
        tempTotal += len(category.entryList)
    print "Total entry count: " + str(tempTotal)

def syllableStatsCommand(shouldSort):
    readDictionaryFile()
    tempSyllableCountMap = {}
    for syllable in syllableSet:
        tempSyllableCountMap[syllable] = 0
    for category in categoryList:
        if category.syllable is not None:
            for entry in category.entryList:
                tempWord = entry.word
                if tempWord is not None:
                    tempSyllable = tempWord[(len(tempWord) - 2):len(tempWord)]
                    tempSyllableCountMap[tempSyllable] += 1
    tempPairList = []
    for syllable in syllableSet:
        tempCount = tempSyllableCountMap[syllable]
        tempPairList.append([syllable, tempCount])
    if shouldSort:
        tempPairList.sort(compareTextCountPair)
    for pair in tempPairList:
        tempSyllable = pair[0]
        tempCount = pair[1]
        printBarMetric(tempSyllable, tempCount, 10, 20)

def consonantStatsCommand():
    readDictionaryFile()
    tempConsonantCountMap = {}
    for consonant in consonantSet:
        tempConsonantCountMap[consonant] = 0
    for category in categoryList:
        if category.syllable is not None:
            for entry in category.entryList:
                tempWord = entry.word
                if tempWord is not None:
                    tempConsonant = tempWord[(len(tempWord) - 2):(len(tempWord) - 1)]
                    tempConsonantCountMap[tempConsonant] += 1
    tempPairList = []
    for consonant in tempConsonantCountMap:
        tempCount = tempConsonantCountMap[consonant]
        tempPairList.append([consonant, tempCount])
    tempPairList.sort(compareTextCountPair)
    for pair in tempPairList:
        tempConsonant = pair[0]
        tempCount = pair[1]
        printBarMetric(tempConsonant, tempCount / 2, 10, 50)

def printCliUsageAndQuit():
    tempScriptPath = "./entryDigest.py"
    print "Usage:"
    print tempScriptPath + " countEntries"
    print tempScriptPath + " categorySyllables"
    print tempScriptPath + " categoryWords (syllable or \"none\")"
    print tempScriptPath + " duplicateWords"
    print tempScriptPath + " verifySyllables"
    print tempScriptPath + " wordExists (word)"
    print tempScriptPath + " syllableStats (should sort)"
    print tempScriptPath + " consonantStats"
    print tempScriptPath + " verifyAll"
    sys.exit(0)

print "Entry Digest"

if len(sys.argv) < 2:
    printCliUsageAndQuit()

commandName = sys.argv[1]

if commandName == "countEntries":
    countEntriesCommand()
elif commandName == "categorySyllables":
    categorySyllablesCommand()
elif commandName == "categoryWords":
    if len(sys.argv) < 3:
        printCliUsageAndQuit()
    tempSyllable = sys.argv[2].upper()
    if tempSyllable == "NONE":
        tempSyllable = None
    categoryWordsCommand(tempSyllable)
elif commandName == "duplicateWords":
    duplicateWordsCommand()
elif commandName == "verifySyllables":
    verifySyllablesCommand()
elif commandName == "wordExists":
    if len(sys.argv) < 3:
        printCliUsageAndQuit()
    tempWord = sys.argv[2].upper()
    wordExistsCommand(tempWord)
elif commandName == "syllableStats":
    if len(sys.argv) < 3:
        shouldSort = True
    else:
        shouldSort = (int(sys.argv[2]) != 0)
    syllableStatsCommand(shouldSort)
elif commandName == "consonantStats":
    consonantStatsCommand()
elif commandName == "verifyAll":
    verifyAllCommand()
else:
    printCliUsageAndQuit()

print "Finished."


