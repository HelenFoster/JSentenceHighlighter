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

def highlightSentences():
    import jsentencehighlighter.run as run
    reload (run)
    run.highlightSentences()

action = QAction("Highlight sentences", mw)
mw.connect(action, SIGNAL("triggered()"), highlightSentences)
mw.form.menuTools.addAction(action)
