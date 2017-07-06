# -*- coding: utf-8 -*-
# Copyright (C) 2017  Helen Foster
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import core, config

if __name__ == "__main__":
    wf = core.WordFinder(config)
    for word in wf.makeInflections(u"食べる", "any", 2):
        print word
    print
    print wf.processSentence(u"茄子", u"なす", u"なすもついかできますか。")["new sentence"]
