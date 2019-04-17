# -*- coding: utf-8 -*-
# Copyright (C) 2017  Helen Foster
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

class WordFinder:
    def __init__(self, conf):
        self.conf = conf
        self.doneAlreadyFinder = re.compile(conf.doneAlreadyRegex)
        with open(conf.deinflectionFile) as f:
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

    def makeInflections(self, word, wordType, depth):
        results = [word]
        if depth == 0 or wordType == "end":
            return results
        for rule in self.rules:
            if word.endswith(rule["kanaRaw"]):
                if wordType == "any" or wordType in rule["typesRaw"]:
                    newWord = word[:-len(rule["kanaRaw"])] + rule["kanaInf"]
                    results.extend(self.makeInflections(newWord, rule["typeInf"], depth-1))
        return results

    def findWord(self, word, sentence):
        if word == "":
            return None
        word = katakanaToHiragana(word)
        sentence = katakanaToHiragana(sentence)
        conjs = self.makeInflections(word, "any", self.conf.maxInflectionDepth)
        conjs.sort(key=len, reverse=True)
        for conj in conjs:
            if conj in sentence:
                return (sentence.index(conj), len(conj))
        return None

    def processSentence(self, word1, word2, sentence):
        result = {}
        result["new sentence"] = sentence
        result["matched"] = False
        if sentence == "":
            result["desc"] = "empty sentence"
        elif self.doneAlreadyFinder.search(sentence) is not None:
            result["desc"] = "done already"
        else:
            match = self.findWord(word1, sentence)
            if match is not None:
                result["desc"] = "word 1 match"
            else:
                match = self.findWord(word2, sentence)
                if match is not None:
                    result["desc"] = "word 2 match"
            if match is None:
                result["desc"] = "no match"
            else:
                (pos, length) = match
                result["new sentence"] = sentence[:pos] + self.conf.startTag
                result["new sentence"] += sentence[pos:pos+length]
                result["new sentence"] += self.conf.endTag + sentence[pos+length:]
                result["matched"] = True
        return result

