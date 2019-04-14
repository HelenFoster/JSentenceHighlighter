# -*- coding: utf-8 -*-
# Copyright (C) 2017  Helen Foster
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

import os, datetime, collections, json
from aqt import mw
from PyQt4.QtGui import QMessageBox

def highlightSentences(browserNids=None):
    import jsentencehighlighter.core as core
    reload (core)
    import jsentencehighlighter.config as conf
    reload (conf)
    
    model = mw.col.models.byName(conf.noteType)
    if model is None:
        QMessageBox.warning(mw, conf.progName, "Can't find note type")
        return
    fieldNames = [fld["name"] for fld in model["flds"]]
    if conf.wordField1 not in fieldNames:
        QMessageBox.warning(mw, conf.progName, "Can't find word field 1")
        return
    if conf.wordField2 is not None and conf.wordField2 not in fieldNames:
        QMessageBox.warning(mw, conf.progName, "Can't find word field 2")
        return
    if conf.sentenceField not in fieldNames:
        QMessageBox.warning(mw, conf.progName, "Can't find sentence field")
        return
    if conf.targetField is not None and conf.targetField not in fieldNames:
        QMessageBox.warning(mw, conf.progName, "Can't find target field")
        return
    
    outcomeCounts = collections.Counter()
    usableNids = mw.col.findNotes("mid:" + str(model["id"]))
    if browserNids is None:
        nids = usableNids
    else:
        usableNids = set(usableNids)
        #keeping browserNids order here for log file, but not sure if it means anything
        nids = [nid for nid in browserNids if nid in usableNids]
        outcomeCounts["wrong type"] = len(browserNids) - len(nids)
    if nids == []:
        QMessageBox.warning(mw, conf.progName, "No notes to process")
        return
    
    if conf.targetField is not None:
        reply = QMessageBox.question(mw, conf.progName,
            "Really overwrite %s for %d notes?" % (conf.targetField, len(nids)),
            QMessageBox.Yes, QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        mw.checkpoint("Highlight sentences") #undo
    
    try:
        wordFinder = core.WordFinder(conf)
    except IOError:
        QMessageBox.warning(mw, conf.progName, "Can't load inflection dictionary")
        return
    
    currentTime = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
    logName = conf.progName + "_%s.log" % currentTime
    logPath = os.path.normpath(os.path.join(mw.col.media.dir(), "..", logName)) #in user profile folder
    mw.progress.start(label="Working...", immediate=True)
    
    try:
        with open(logPath, "w") as logFile:
            for nid in nids:
                note = mw.col.getNote(nid)
                sentence = note[conf.sentenceField]
                word1 = note[conf.wordField1]
                word2 = "" if conf.wordField2 is None else note[conf.wordField2]
                result = wordFinder.processSentence(word1, word2, sentence)
                outcomeCounts[result["desc"]] += 1
                logLine = result["desc"] + "\t" + word1 + "\t" + word2 + "\t" + result["new sentence"] + "\n"
                logFile.write(logLine.encode("utf-8"))
                if conf.targetField is not None:
                    #Update note. Not the shortest way to write this, but want to be clear!
                    if conf.targetField == conf.sentenceField:
                        #Overwriting original field.
                        #Update note and add the tag if sentence has changed.
                        #Leave tag if it was there already - 
                        # multiple runs with changed program will add to previous results.
                        if result["matched"]:
                            note[conf.targetField] = result["new sentence"]
                            note.addTag(conf.matchedTag)
                    else:
                        #Overwriting a different field.
                        #Update every note. Add the tag if sentence has changed.
                        #Remove tag if no match - 
                        # multiple runs with changed program will overwrite previous results.
                        note[conf.targetField] = result["new sentence"]
                        if result["matched"]:
                            note.addTag(conf.matchedTag)
                        else:
                            note.delTag(conf.matchedTag)
                    note.flush()
            logFile.write("\nTOTALS\n")
            for outcome in ["word 1 match", "word 2 match", "no match", "done already", "empty sentence", "wrong type"]:
                logFile.write(outcome + "\t" + str(outcomeCounts[outcome]) + "\n")
            mw.progress.finish()
            QMessageBox.information(mw, conf.progName, "Done")
    except IOError:
        mw.progress.finish()
        QMessageBox.warning(mw, conf.progName, "Error writing log file")
