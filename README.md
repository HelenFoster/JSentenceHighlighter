JSentenceHighlighter
====================

Anki addon for use with a Japanese vocab+sentence deck. For each note, it searches for the vocab word in the sentence, and marks it in the sentence according to the user's preference.

Yomichan can now mark the target word in the sentence when adding the card, and that is preferable because no guessing is required. But this addon could be useful for Yomichan users who want to fill in the sentence highlighting on old cards created before the feature was available.

This project is licensed under the GNU AGPL, version 3 or later ( http://www.gnu.org/licenses/agpl.html ).

The file deinflect.json is taken from the Yomichan project ( https://foosoft.net/projects/yomichan/ ) and was originally based on data from Rikaichan ( http://www.polarcloud.com/rikaichan ).

Instructions
------------

Be very careful with this! Back up your collection before starting, and be really sure that the addon has done what you intended before continuing with reviews.

Copy JSentenceHighlighter.py and the jsentencehighlighter directory into the Anki addons directory.

Edit config.py to match your deck. See the comments in the file for what each variable means.

Restart Anki and "Highlight sentences" should appear on the Tools menu. This runs the highlighting operation as defined in config.py. (The config is auto-reloaded at the start of each run, so you don't need to restart Anki again after changing something.)

After each run, the addon places a timestamped log file in your Anki profile directory. Running with targetField=None doesn't change your deck, so you can look at this file to see what is going to be done.

