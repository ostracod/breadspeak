#!/usr/bin/env python

import sys
from copy import deepcopy
import json

dictionaryPath = "./dictionary.txt"
verificationPath = "./verification.txt"
dictionaryJsonPath = "./dictionary.json"
categorySyllableSet = ["BA", "BE", "DA", "DE", "FA", "FE", "GA", "GE", "KA", "KE", "PA", "PE", "SA", "SE", "TA", "TE", "VA", "VE", "ZA", "ZE"]
consonantSet = ["B", "D", "F", "G", "K", "P", "S", "T", "V", "Z"]
vowelSet = ["A", "E", "I", "O", "U"]
antonymVowelPairSet = {"E": "I", "A": "U", "I": "E", "U": "A"}
categoryList = []
legendLineList = []
syllableSet = []
verificationList = []

for consonant in consonantSet:
    for vowel in vowelSet:
        syllableSet.append(consonant + vowel)

def isEntryLine(line):
    return (line.find("): ") >= 0)

def isCategoryLine(line):
    return (line.find("> ") == 0)

def isVerificationLine(line):
    return (line.find(": ") >= 0 and line.find(" (") >= 0)

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

def getAntonymWord(word):
    tempVowel = word[1]
    tempVowel = antonymVowelPairSet[tempVowel]
    return word[0] + tempVowel + word[2:len(word)]

def parseKeywords(definition):
    output = []
    while True:
        tempStartIndex = definition.find("~")
        if tempStartIndex < 0:
            break
        tempEndIndex = tempStartIndex + 1
        while tempEndIndex < len(definition):
            tempCharacter = ord(definition[tempEndIndex])
            # Not A-Z or a-z.
            if not ((tempCharacter >= 65 and tempCharacter <= 90) \
                    or (tempCharacter >= 97 and tempCharacter <= 122)):
                break
            tempEndIndex += 1
        output.append(definition[(tempStartIndex + 1):tempEndIndex])
        definition = definition[0:tempStartIndex] + definition[(tempStartIndex + 1):len(definition)]
    return (definition, output)

class Entry(object):
    
    def __init__(self, line):
        self.keywordList = []
        tempStartIndex = line.find("{")
        if tempStartIndex > 0:
            tempEndIndex = line.rfind("}")
            tempMetadata = json.loads(line[tempStartIndex:(tempEndIndex + 1)])
            line = line[0:tempStartIndex] + line[(tempEndIndex + 1):len(line)]
            if "extraKeywords" in tempMetadata:
                for keyword in tempMetadata["extraKeywords"]:
                    self.keywordList.append(str(keyword))
        index = line.find("(");
        if index > 0:
            self.word = line[0:(index - 1)].upper()
        else:
            self.word = None
        tempEndIndex = line.find("): ")
        self.partOfSpeech = line[(index + 1):tempEndIndex]
        self.definition = line[(tempEndIndex + 3):len(line)]
        index = self.definition.find("(*):")
        if index >= 0:
            index2 = self.definition.rfind(".", 0, index)
            self.antonymWord = self.definition[(index2 + 2):(index - 1)].upper()
            self.antonymDefinition = self.definition[(index + 5):len(self.definition)]
            self.definition = self.definition[0:(index2 + 1)]
            self.hasAntonym = True
        else:
            self.hasAntonym = False
        self.definition, tempKeywordList = parseKeywords(self.definition)
        self.keywordList.extend(tempKeywordList)
        if len(self.keywordList) > 0:
            print self.definition
            print self.keywordList
    
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
    
    def toJsonData(self):
        if self.hasAntonym:
            tempAntonym = {
                "word": self.antonymWord,
                "definition": self.antonymDefinition
            }
        else:
            tempAntonym = None
        return {
            "word": self.word,
            "partOfSpeech": self.partOfSpeech,
            "definition": self.definition,
            "antonym": tempAntonym
        }

class Category(object):
    
    def __init__(self, line):
        self.name = getLineCategoryName(line)
        self.syllable = getLineCategorySyllable(line)
        self.entryList = []
    
    def addEntry(self, entry):
        self.entryList.append(entry)
    
    def containsWord(self, word):
        word = word.upper()
        for entry in self.entryList:
            if entry.word is not None:
                if entry.word == word:
                    return True
        return False
    
    def toJsonData(self):
        entryJsonDataList = []
        for entry in self.entryList:
            entryJsonDataList.append(entry.toJsonData())
        return {
            "name": self.name,
            "syllable": self.syllable,
            "entries": entryJsonDataList
        }

class Verification(object):
    
    def __init__(self, line):
        line = line.upper()
        index1 = line.index(": ")
        index2 = line.index(" (")
        index3 = line.index(")")
        self.original = line[0:index1]
        tempText = line[(index1 + 2):index2]
        self.translation = tempText.split(" ")
        self.gloss = line[(index2 + 2):index3]
    
    def toString(self):
        return "%s: %s (%s)" % (self.original, " ".join(self.translation), self.gloss)

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
    tempIsInLegend = False
    for line in tempList:
        if isCategoryLine(line):
            tempCategory = Category(line)
            categoryList.append(tempCategory)
            tempLastCategory = tempCategory
            tempIsInLegend = False
        if isEntryLine(line):
            tempEntry = Entry(line)
            tempLastCategory.addEntry(tempEntry)
        if tempIsInLegend:
            if len(line) > 0:
                legendLineList.append(line)
        elif line == "LEGEND_START":
            tempIsInLegend = True

def readVerificationFile():
    with open(verificationPath, "r") as file:
        inputText = file.read()
    tempList = inputText.split("\n")
    for line in tempList:
        if isVerificationLine(line):
            tempVerification = Verification(line)
            verificationList.append(tempVerification)

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
    verifyAntonyms()
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

def missingWordsCommand(secondSyllable=None):
    readDictionaryFile()
    for category in categoryList:
        if secondSyllable is not None:
            if category.syllable is None:
                tempWord = secondSyllable
            else:
                tempWord = category.syllable + secondSyllable
            if category.containsWord(tempWord):
                continue
        for entry in category.entryList:
            tempWord = entry.word
            if tempWord is None:
                print category.syllable + "__ " + entry.toString()

def secondSyllableCommand(secondSyllable):
    readDictionaryFile()
    for category in categoryList:
        for entry in category.entryList:
            tempWord = entry.word
            if tempWord is not None:
                tempSyllable = tempWord[(len(tempWord) - 2):len(tempWord)]
                if tempSyllable == secondSyllable:
                    print entry.toString()

def analyzeVerificationCommand():
    readDictionaryFile()
    readVerificationFile()
    tempUnusedEntryList = []
    tempValidWordSet = {}
    tempInvalidWordList = []
    for category in categoryList:
        for entry in category.entryList:
            tempUnusedEntryList.append(entry)
            tempValidWordSet[entry.word] = True
            if entry.hasAntonym:
                tempValidWordSet[entry.antonymWord] = True
    for verification in verificationList:
        for word in verification.translation:
            if word not in tempValidWordSet:
                tempInvalidWordList.append(word)
            # Something something bad time complexity
            # I don't care in this context
            index = 0
            while index < len(tempUnusedEntryList):
                tempEntry = tempUnusedEntryList[index]
                tempShouldRemove = False
                if word == tempEntry.word:
                    tempShouldRemove = True
                elif tempEntry.hasAntonym:
                    if word == tempEntry.antonymWord:
                        tempShouldRemove = True
                if tempShouldRemove:
                    del tempUnusedEntryList[index]
                    break
                index += 1
    print "Unused words in verification:"
    for entry in tempUnusedEntryList:
        print entry.toString()
    print "Invalid verification words:"
    print tempInvalidWordList

def verifyAntonyms():
    tempBadWordList = []
    for category in categoryList:
        for entry in category.entryList:
            if entry.hasAntonym:
                tempWord = getAntonymWord(entry.word)
                if tempWord != entry.antonymWord:
                    tempBadWordList.append(entry.word)
    print "Words with bad antonyms:"
    print tempBadWordList

def verifyAntonymsCommand():
    readDictionaryFile()
    verifyAntonyms()

def getJsonCommand():
    readDictionaryFile()
    categoryJsonDataList = []
    for category in categoryList:
        categoryJsonDataList.append(category.toJsonData())
    with open(dictionaryJsonPath, "w") as file:
        json.dump({
            "legend": legendLineList,
            "categories": categoryJsonDataList
        }, file)

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
    print tempScriptPath + " missingWords (second syllable?)"
    print tempScriptPath + " secondSyllable (syllable)"
    print tempScriptPath + " verifyAll"
    print tempScriptPath + " analyzeVerification"
    print tempScriptPath + " verifyAntonyms"
    print tempScriptPath + " getJson (destination path)"
    sys.exit(0)

print "Starting entry digest..."

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
elif commandName == "analyzeVerification":
    analyzeVerificationCommand()
elif commandName == "missingWords":
    if len(sys.argv) < 3:
        secondSyllable = None
    else:
        secondSyllable = sys.argv[2]
    missingWordsCommand(secondSyllable=secondSyllable)
elif commandName == "secondSyllable":
    if len(sys.argv) < 3:
        printCliUsageAndQuit()
    tempSyllable = sys.argv[2].upper()
    secondSyllableCommand(tempSyllable)
elif commandName == "verifyAll":
    verifyAllCommand()
elif commandName == "verifyAntonyms":
    verifyAntonymsCommand()
elif commandName == "getJson":
    getJsonCommand()
else:
    printCliUsageAndQuit()

print "Finished entry digest."


