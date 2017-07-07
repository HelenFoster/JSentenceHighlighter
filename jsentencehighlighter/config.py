# -*- coding: utf-8 -*-
# Copyright (C) 2017  Helen Foster
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import os

#If the sentence matches this, it will be left alone.
doneAlreadyRegex = "<b>"

#These will be inserted before and after the matched word.
startTag = "<b>"
endTag = "</b>"

#Note type to modify.
noteType = "vocab"

#High priority word field (usually the expression field).
wordField1 = "expression"

#Low priority word field (usually the reading field) - can be None.
wordField2 = "kana"

#Field to get the original sentence from.
sentenceField = "yc-sentence"

#Field to write the results - WILL BE OVERWRITTEN - set to None for a dry run.
#(Can be the same as sentenceField - this changes tagging behaviour.)
targetField = None

#Program name used in messages and the log filename.
progName = "JSentenceHighlighter"

#Anki tag to add to matched notes.
matchedTag = "JSH-matched"

#Maximum number of inflections to apply to a word at one time.
#Runtime will increase exponentially with this number!
#2 is enough for the vast majority of cases.
maxInflectionDepth = 2

#Path to the deinflection dictionary.
deinflectionFile = os.path.join(os.path.dirname(os.path.realpath(__file__)), "deinflect.json")
