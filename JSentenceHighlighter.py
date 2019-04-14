# -*- coding: utf-8 -*-
# Copyright (C) 2017  Helen Foster
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

# JSentenceHighlighter is an Anki addon for a Japanese vocab+sentence deck.
# It searches and marks the vocab word in the sentence.
# This file belongs with the "jsentencehighlighter" folder:
#  the README might be inside depending on how you received this!

from aqt import mw
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QAction
from anki.hooks import addHook

def highlightSentences(nids=None):
    import jsentencehighlighter.run as run
    reload (run)
    run.highlightSentences(nids)

action = QAction("Highlight all sentences (JSH)", mw)
mw.connect(action, SIGNAL("triggered()"), highlightSentences)
mw.form.menuTools.addAction(action)

def addToBrowserMenu(browser):
    def highlightSelected():
        highlightSentences(browser.selectedNotes())
    action = QAction("Highlight selected sentences (JSH)", browser)
    browser.connect(action, SIGNAL("triggered()"), highlightSelected)
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(action)

addHook("browser.setupMenus", addToBrowserMenu)
