# -*- coding: utf-8 -*-
# Copyright (C) 2017,2019  Helen Foster
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import unittest2
import core, config

class TestWordFinder(unittest2.TestCase):
    def test_processSentence(self):
        cases = [
            (([u"a"],   u"aaa", True), u"<b>a</b><b>a</b><b>a</b>"),
            (([u"aa"],  u"aaa", True), u"<b>aa</b>a"),
            (([u"aa"],  u"aaaaa", True), u"<b>aa</b><b>aa</b>a"),
            (([u"aa"],  u"aaaaa", False), u"<b>aa</b>aaa"),
            (([u"aba"], u"abaaba", True), u"<b>aba</b><b>aba</b>"),
            (([u"aba"], u"ababa", True), u"<b>aba</b>ba"),
            (([u"aa"],  u"aa[xx]", True), u"<b>aa[xx]</b>"),
            (([u"aa"],  u"xx[aa]", True), u"xx[aa]"),
            (([u"aa"],  u"aa[xx] aa[xx]", True), u"<b>aa[xx]</b><b> aa[xx]</b>"),
            (([u"a"],   u"a[xx] aa[xx]", True), u"<b>a[xx]</b><b> aa[xx]</b>"),
            (([u"bb"],  u"a abb[xxx]a bba[xxx]a", True), u"a<b> abb[xxx]</b>a<b> bba[xxx]</b>a"),
            (([u"茄子", u"なす"], u"なすもついかできますか。", True), u"<b>なす</b>もついかできますか。"),
        ]
        for i in range(len(cases)):
            with self.subTest(i=i):
                (params, result) = cases[i]
                newSentence = wf.processSentence(*params)["new sentence"]
                self.assertEqual(newSentence, result)

if __name__ == "__main__":
    wf = core.WordFinder(config)
    for word in wf.makeInflectionsRec(u"食べる", "any", 2):
        print(word)
    print("")
    nakuText = u"ニャーニャー泣いていた事だけは記憶している。しばらくして泣いたら書生がまた迎に来てくれるかと考え付いた。" \
        + u"なきたくても声が出ない。大きな声で泣き出すのである。"
    trials = [
        ([u"泣く"], nakuText, True),
        ([u"泣く"], nakuText, False),
        ([u"なく"], nakuText, True),
        ([u"泣く", u"なく"], nakuText, True),
    ]
    for trial in trials:
        (words, sentence, matchAll) = trial
        newSentence = wf.processSentence(*trial)["new sentence"]
        print(u" ".join(words) + "\t" + str(matchAll) + "\n" + newSentence)
    unittest2.main()
