# evernote-dump

Get all of your attachments out of your exported Evernote enex file and include the correct file dates.

Evernote-dump works by streaming the .enex file through a parser so even extremely large .enex files should work.

# Installation

Before running the Evernote.py script be sure to install.

pip install filemagic

# Instructions

Run using

> python Evernote.py FILE.enex

All the files found in the enex files will be put in the "output" folder

# Road Map

  -[x] Export all attachements
  -[x] Keep the modified dates
  -[x] Keep file names if desired
  -[ ] Export actual notes
  -[ ] Convert notes to mark down
  -[ ] Make compatible with QownNotes
