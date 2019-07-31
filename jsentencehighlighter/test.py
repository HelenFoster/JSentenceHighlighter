# -*- coding: utf-8 -*-
# Copyright (C) 2017,2019  Helen Foster
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import core, config

if __name__ == "__main__":
    wf = core.WordFinder(config)
    for word in wf.makeInflectionsRec(u"食べる", "any", 2):
        print(word)
    print("")
    nakuText = u"ニャーニャー泣いていた事だけは記憶している。しばらくして泣いたら書生がまた迎に来てくれるかと考え付いた。" \
        + u"なきたくても声が出ない。大きな声で泣き出すのである。"
    trials = [
        ([u"aa"], u"aaa", True),
        ([u"aa"], u"aaaaa", True),
        ([u"aa"], u"aaaaa", False),
        ([u"aba"], u"abaaba", True),
        ([u"aba"], u"ababa", True),
        ([u"茄子", u"なす"], u"なすもついかできますか。", True),
        ([u"泣く"], nakuText, True),
        ([u"泣く"], nakuText, False),
        ([u"なく"], nakuText, True),
        ([u"泣く", u"なく"], nakuText, True),
    ]
    for trial in trials:
        (words, sentence, matchAll) = trial
        newSentence = wf.processSentence(*trial)["new sentence"]
        print(u" ".join(words) + "\t" + str(matchAll) + "\n" + newSentence)
