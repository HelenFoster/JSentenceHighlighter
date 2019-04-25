# -*- coding: utf-8 -*-
# Copyright (C) 2017,2019  Helen Foster
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import re, json

katakanaToHiraganaTable = {}
try:
    unichr
except NameError:
    unichr = chr
for hIndex in range(0x3041, 0x3097):
    katakanaToHiraganaTable[unichr(hIndex+0x60)] = unichr(hIndex)

def katakanaToHiragana(s):
    return "".join([katakanaToHiraganaTable.get(ch, ch) for ch in s])

def addMatch(matches, start, end):
    for (s1, e1) in matches:
        #prevent overlapping matches
        if end > s1 and start < e1:
            return
    matches.append((start, end))

class WordFinder:
    def __init__(self, conf):
        self.conf = conf
        self.doneAlreadyFinder = re.compile(conf.doneAlreadyRegex)
        with open(conf.deinflectionFile, "rb") as f:
            srcdic = json.load(f)
        self.rules = []
        for reason in srcdic:
            for rule in srcdic[reason]:
                newRule = {}
                newRule["kanaRaw"] = rule["kanaOut"]
                newRule["kanaInf"] = rule["kanaIn"]
                newRule["typesRaw"] = rule["rulesOut"]
                
                if newRule["kanaRaw"] == "":
                    continue  #skipping -na (not needed and causes problems)
                
                nRI = len(rule["rulesIn"])
                if nRI == 0:
                    newRule["typeInf"] = "end"
                elif nRI == 1:
                    newRule["typeInf"] = rule["rulesIn"][0]
                else:
                    raise ValueError("Inflected word has more than one type")
                
                self.rules.append(newRule)

    def makeInflectionsRec(self, word, wordType, depth):
        results = [word]
        if depth == 0 or wordType == "end":
            return results
        for rule in self.rules:
            if word.endswith(rule["kanaRaw"]):
                if wordType == "any" or wordType in rule["typesRaw"]:
                    newWord = word[:-len(rule["kanaRaw"])] + rule["kanaInf"]
                    results.extend(self.makeInflectionsRec(newWord, rule["typeInf"], depth-1))
        return results

    def makeInflections(self, word):
        if word == "":
            return []
        conjs = self.makeInflectionsRec(word, "any", self.conf.maxInflectionDepth)
        conjs.sort(key=len, reverse=True)
        return conjs

    def findWord(self, word1, word2, sentence, matchAll):
        matches = []
        word1 = katakanaToHiragana(word1)
        word2 = katakanaToHiragana(word2)
        sentence = katakanaToHiragana(sentence)
        conjs = self.makeInflections(word1) + self.makeInflections(word2)
        for conj in conjs:
            cursor = 0
            while cursor < len(sentence):
                startPos = sentence.find(conj, cursor)
                if startPos == -1:
                    break
                endPos = startPos + len(conj)
                addMatch(matches, startPos, endPos)
                if not matchAll:
                    return matches
                cursor = endPos
        return matches

    def processSentence(self, word1, word2, sentence, matchAll=None):
        result = {}
        result["new sentence"] = sentence
        result["matched"] = False
        if sentence == "":
            result["desc"] = "empty sentence"
        elif self.doneAlreadyFinder.search(sentence) is not None:
            result["desc"] = "done already"
        else:
            if matchAll is None:
                try:
                    #don't crash if using old config
                    matchAll = self.conf.matchAll
                except:
                    matchAll = False
            matches = self.findWord(word1, word2, sentence, matchAll)
            if matches == []:
                result["desc"] = "no match"
            else:
                result["desc"] = "match found"
                result["matched"] = True
                matches.sort()
                cursor = 0
                result["new sentence"] = ""
                for (start, end) in matches:
                    result["new sentence"] += sentence[cursor:start] + self.conf.startTag
                    result["new sentence"] += sentence[start:end] + self.conf.endTag
                    cursor = end
                result["new sentence"] += sentence[cursor:]
        return result

