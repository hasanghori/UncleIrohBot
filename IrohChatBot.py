from flask import Flask
from datetime import timedelta
import time

from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
import random


def turnScriptIntoArray():
    linesToConvert = []
    f = open("everyUncleIrohLine.txt", "r")
    fline = f.readlines()
    for x in fline:  #
        linesToConvert.append(x)
    lines = [["" for x in range(200)] for y in range(len(linesToConvert) + 1)]
    lengthOfData = len(linesToConvert)
    stringAdd = ""
    z = int(0)
    for x in range(0, len(linesToConvert)):
        string = linesToConvert[x]
        z = int(0)
        for y in range(0, len(string)):
            if string[y] == " " or string[y] == "\n" or string[y] == "." or string[y] == "!" or string[y] == ",":
                lines[x][z] = stringAdd
                stringAdd = ""
                z = z + 1
            else:
                stringAdd = stringAdd + string[y]
            if string[y] == "." or string[y] == "!" or string[y] == ",":
                lines[x][z] = string[y]
                z = z + 1
    return lines

def initialFindWordToUse(lines, keyWord):
    try:
        if (keyWord == 'you'):
            keyWord = 'I'
        
        wordsAfter = []
        wordsBefore = []
        for line in lines:
            for wordIdx in range(0, len(line)):
                if line[wordIdx] == keyWord:
                    if wordIdx != len(line) - 1:
                        wordsAfter.append(line[wordIdx + 1])
                    if wordIdx != 0:
                        wordsBefore.append(line[wordIdx - 1])
                    else:
                        wordsBefore.append("")
        if len(wordsAfter) == 0 and len(wordsBefore) == 0:
            print("problemo")
        return buildSentence(wordsBefore, wordsAfter, keyWord, lines)
    except:
        wordRandom = ""
        while wordRandom == "":
            lineRandom = random.choice(lines)
            wordRandom = random.choice(lineRandom)
        oldKeyWord = keyWord
        keyWord = wordRandom
        wordsAfter = []
        wordsBefore = []
        for line in lines:
            for wordIdx in range(0, len(line)):
                if line[wordIdx] == keyWord:
                    if wordIdx != len(line) - 1:
                        wordsAfter.append(line[wordIdx + 1])
                    if wordIdx != 0:
                        wordsBefore.append(line[wordIdx - 1])
                    else:
                        wordsBefore.append("")
        if len(wordsAfter) == 0 and len(wordsBefore) == 0:
            print("problemo")

        return "I don't understand the word '" + oldKeyWord + "' so here is some random advice. " + buildSentence(wordsBefore, wordsAfter, keyWord, lines)

def buildSentence(wordsBefore, wordsAfter, keyWord, lines):
    beforeWord = random.choice(wordsBefore)
    afterWord = random.choice(wordsAfter)
    sentence = [keyWord]
    finalSentence = ""
    while beforeWord != "" or afterWord != "":
        sentence.insert(0, beforeWord)
        sentence.append(afterWord)
        if afterWord != "":
            wordsAfter = findWordAfter(sentence, lines)
            #afterWord = max(set(wordsAfter), key=wordsAfter.count)
            afterWord = random.choice(wordsAfter)
        if beforeWord != "":
            wordsBefore = findWordsBefore(sentence, lines)
            beforeWord = random.choice(wordsBefore)
    for word in sentence:
        finalSentence = finalSentence + word + " "
    return finalSentence

def findWordAfter(sentence, lines):
    wordsAfter = []
    keyWord = sentence[len(sentence) - 1]
    for line in lines:
        for wordIdx in range(1, len(line)):
            if line[wordIdx] == keyWord:
                if line[wordIdx - 1] == sentence[len(sentence) - 2]:
                    if wordIdx != len(line) - 1:
                        wordsAfter.append(line[wordIdx + 1])
    return wordsAfter

def findWordsBefore(sentence, lines):
    wordsBefore = []
    keyWord = sentence[0]
    for line in lines:
        for wordIdx in range(0, len(line) - 1):
            if line[wordIdx] == keyWord:
                if line[wordIdx + 1] == sentence[1]:
                    if wordIdx != 0:
                        wordsBefore.append(line[wordIdx - 1])
                    else:
                        wordsBefore.append("")
    return wordsBefore
def run(question):
    question = question.split(" ")
    word = question[len(question) - 1].split("?")
    keyWord = word[0]
    lines = turnScriptIntoArray()

    return initialFindWordToUse(lines, keyWord)


question = ""
while question != "no":
    question = input("ask uncle iroh a question")
    print(run(question))
#question = question.split(" ")
#word = question[len(question) - 1].split("?")
#keyWord = word[0]
#lines = turnScriptIntoArray()
#print(initialFindWordToUse(lines, keyWord))

