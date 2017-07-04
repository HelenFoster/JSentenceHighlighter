# -*- coding: utf-8 -*-
# Copyright (C) 2017  Helen Foster
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

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
