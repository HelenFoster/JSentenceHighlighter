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
        (u"茄子", u"なす", u"なすもついかできますか。", True),
        (u"泣く", u"なく", nakuText, False),
        (u"泣く", u"なく", nakuText, True),
        (u"泣く", u"", nakuText, True),
        (u"", u"なく", nakuText, True),
    ]
    for trial in trials:
        (word1, word2, sentence, matchAll) = trial
        newSentence = wf.processSentence(*trial)["new sentence"]
        print(word1 + "\t" + word2 + "\t" + str(matchAll) + "\n" + newSentence)
