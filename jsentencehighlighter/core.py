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

class SentenceMatches:
    #regex based on Anki's furigana.py, but detect non-breaking spaces without replacing:
    furiganaRegex = re.compile(r'(?:&nbsp;| )?([^ >]+?)\[(.+?)\]')
    def __init__(self, sentence, matchAll):
        self.sentence = sentence
        self.matchAll = matchAll
        mIter = SentenceMatches.furiganaRegex.finditer(sentence)
        self.furiganaGroups = [m for m in mIter if not m.group(2).startswith("sound:")]
        self.kanji = ""
        cursor = 0
        for m in self.furiganaGroups:
            self.kanji += sentence[cursor:m.start()] + m.group(1)
            cursor = m.end()
        self.kanji += sentence[cursor:]
        self.matches = []
    def remap(self, start, end):
        #translate kanji matches back to full sentence with furigana
        for fGroup in self.furiganaGroups:
            fStart = fGroup.start()
            fEnd = fGroup.end()
            fLength = fEnd - fStart
            fOffset = fLength - len(fGroup.group(1))
            if start + fOffset >= fEnd:
                #word is after this furigana group
                #account for the extra characters and keep going
                start += fOffset
                end += fOffset
            elif end > fStart:
                #overlaps this furigana group (overlap: end > start2 and start < end2)
                #expand match to cover furigana (so highlight doesn't break rendering)
                end += fOffset
                if start > fStart:
                    start = fStart
                if end < fEnd:
                    end = fEnd
                #keep going, in case it overlaps more than one furigana group
            else:
                #word is before this furigana group and the remaining ones
                break
        return (start, end)
    def _add(self, start, end):
        (start, end) = self.remap(start, end)
        for (s1, e1) in self.matches:
            #prevent overlapping matches
            if end > s1 and start < e1:
                return
        self.matches.append((start, end))
    def check(self, conj):
        if self.matches != [] and not self.matchAll:
            return False
        cursor = 0
        found = False
        while cursor < len(self.kanji):
            startPos = self.kanji.find(conj, cursor)
            if startPos == -1:
                return found
            endPos = startPos + len(conj)
            self._add(startPos, endPos)
            cursor = endPos
            found = True
            if not self.matchAll:
                return found
        return found
    def isEmpty(self):
        return self.matches == []
    def __iter__(self):
        self.matches.sort()
        for item in self.matches:
            yield item

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

    def findWord(self, words, sentence, matchAll):
        words = [katakanaToHiragana(word) for word in words]
        sentence = katakanaToHiragana(sentence)
        matches = SentenceMatches(sentence, matchAll)
        conjs = []
        for word in words:
            conjs.extend(self.makeInflections(word))
        for conj in conjs:
            matches.check(conj)
        #could make this more efficient for the match-once case
        return matches

    def processSentence(self, words, sentence, matchAll=None):
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
            matches = self.findWord(words, sentence, matchAll)
            if matches.isEmpty():
                result["desc"] = "no match"
            else:
                result["desc"] = "match found"
                result["matched"] = True
                cursor = 0
                result["new sentence"] = ""
                for (start, end) in matches:
                    result["new sentence"] += sentence[cursor:start] + self.conf.startTag
                    result["new sentence"] += sentence[start:end] + self.conf.endTag
                    cursor = end
                result["new sentence"] += sentence[cursor:]
        return result

