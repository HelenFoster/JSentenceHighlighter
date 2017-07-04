#!/usr/bin/sh

# Run this file from the directory it's in.
# Creates jsentencehighlighter.zip

if [ -e "jsentencehighlighter.zip" ]
then
  echo "Please rename or delete jsentencehighlighter.zip"
  exit
fi

zip -r jsentencehighlighter.zip JSentenceHighlighter.py jsentencehighlighter --exclude \*.pyc
