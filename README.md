# Evernote Dump

Export extract evernote notes and attachments from .enex files.

All notes and attachments will keep their original file created and accessed dates. Notes will be converted to markdown format. Tags and other embedded information will be formatted and added to the end of each note.

Evernote Dump works by streaming the .enex file through a parser so even extremely large .enex files _should_ work.

# Quick Run

Windows: Double click the "Evernote Dump.bat"

# Installation

Before running the evernote_dump.py script be sure to install.

> pip install -r requirements.txt

# Instructions
## GUI:
Run using python 3

> python main.py

## CLI:
Run using python 3:

> python run_script.py FILE.enex  

or for exporting all enex files in a folder, use:  

> python run_script.py *  

it will weed out all other non-enex files. If your system is setup to default to python 2 run using:

> python3 run_script.py FILE.enex

All attachments found will be output the the "ENEX-FILE-NAME-ROOT/media" folder as where you called evernote_dump.py .

All the files found in the enex files will be put in the folder

# TODO

- [x] Export Note Attributes
    - [x] Export Tags
- [x] Allow multiple files and export to seperate folders.
- [x] Export all attachements.
- [x] Keep the modified dates.
- [x] Keep file names if desired.
- [x] Make multilingual just for fun.
    - [x] Add multilingual to processing text.
- [x] Export actual notes.
  - [x] Add links to the images that were extracted.
  - [x] Add resourse attributes.
- [x] Convert notes to mark down.
- [x] Add more error check to combat human errors
- [x] Get rid of cleanup warning.
- [x] Clean up the code!

# Evernote Enex File Map

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE en-export SYSTEM "http://xml.evernote.com/pub/evernote-export3.dtd">
<en-export export-date="20130730T205637Z" application="Evernote" version="Evernote Mac">
    <note>
        <title>Test Note for Export</title>
        <content>
            <![CDATA[<?xml version="1.0" encoding="UTF-8" standalone="no"?>
            <!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">
            <en-note style="word-wrap: break-word; -webkit-nbsp-mode: space; -webkit-line-break: after-white-space;">
                Hello, World.
                <div>
                    <br/>
                </div>
                <div>
                    <en-media alt="" type="image/jpeg" hash="dd7b6d285d09ec054e8cd6a3814ce093"/>
                </div>
            </en-note>
            ]]>
        </content>
        <created>20130730T205204Z</created>
        <updated>20130730T205624Z</updated>
        <tag>fake-tag</tag>
        <note-attributes>
            <latitude>33.88394692352314</latitude>
            <longitude>-117.9191355110099</longitude>
            <altitude>96</altitude>
            <author>exomut</author>
        </note-attributes>
        <resource>
            <data encoding="base64">/9j/4AAQSkZJRgABAQAAAQABAAD/4gxYSUNDX1BST0ZJTEUAAQEAAAxITGlubwIQAABtbnRyUkdCIFhZ
            WiAHzgACAAkABgAxAABhY3NwTVNGVAAAAABJRUMgc1JHQgAAAAAAAAAAAAAAAAAA9tYAAQAAAADTLUhQ
            <!-- ... -->
            kfeIGT/+uufk8DpM0gyVjGfmzkgetesnUoTHJ+5Cxn86zmv4/wB75EW+QHAPUH/P9Ky+s1rtrr/wfvOm
            dBSamnq/xPKp/hpLKmS7x4OBjgn6elee6v4OuLJirRSHb/FtyG9s9u1fR0+oTiIRvGq7W4bpisfUGk1C
            GVWtkIyM57n1rfDY+uqigtU76ffZkUsA6iajHZ6v/P8A4B//2Q==</data>
            <mime>image/jpeg</mime>
            <width>1280</width>
            <height>720</height>
            <resource-attributes>
                <file-name>snapshot-DAE9FC15-88E3-46CF-B744-DA9B1B56EB57.jpg</file-name>
				<source-url>www.google.com</source-url>
            	<latitude>33.88394692352314</latitude>
            	<longitude>-117.9191355110099</longitude>
            	<altitude>96</altitude>
				<camera-make>Sharp</camera-make>
				<camera-model>23</camera-model>
				<attachment>true</attachment> #DOUBLE CHECK
				<application-data>Developer place 4K</application-data>

            </resource-attributes>
        </resource>
    </note>
</en-export>
```
