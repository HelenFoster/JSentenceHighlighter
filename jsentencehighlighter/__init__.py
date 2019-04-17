# -*- coding: utf-8 -*-
# Copyright (C) 2017,2019  Helen Foster
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

# JSentenceHighlighter is an Anki addon for a Japanese vocab+sentence deck.
# It searches and marks the vocab word in the sentence.

from aqt import mw
from aqt.qt import QAction
from anki.hooks import addHook

try:
    from importlib import reload
except:
    pass #Python 2 has reload built-in

def highlightSentences(nids):
    from . import run
    reload(run)
    run.highlightSentences(nids)

def highlightAllSentences():
    #A no-arg version is needed, otherwise new-style signal passes False
    highlightSentences(None)

action = QAction("Highlight all sentences (JSH)", mw)
action.triggered.connect(highlightAllSentences)
mw.form.menuTools.addAction(action)

def addToBrowserMenu(browser):
    def highlightSelected():
        highlightSentences(browser.selectedNotes())
    action = QAction("Highlight selected sentences (JSH)", browser)
    action.triggered.connect(highlightSelected)
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(action)

addHook("browser.setupMenus", addToBrowserMenu)
