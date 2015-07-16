Auditor
=======

Auditor is a simple tool to generate basic text and BBCode formatted reports about your Mac's hardware and software. Why not use System Profiler? This is, arguably, easier, open source and creates pared down reports (contrary to SP which, although great for detail, is a bit much).

This app also produces some BBCode formatted reports (think vBulletin) so if someone requests some details, simply select the "optimize for forums" option.


![Early screenshot of Auditor](http://www.bryanabsmith.com/auditor/screen_pre1.0.png)

Licence
-------

The app itself is &copy; 2015 Bryan Smith.

The icon is courtesy of the Tango Project and is public domain.


Building
--------

Want to build Auditor on your own machine? Here are the build requirements:

* Python >= 2.7 (Python 3 not supported)
* wxPython
* cxfreeze
* OPTIONAL: appdmg (if you want to create a disk image installer).

### Steps
1. Run

        python setup.py bdist_mac

2. Your app bundle will be in build/Auditor-X.X.app (X.X is the version number).
3. If you want to build a disk image installer, simply run the following:

        appdmg appdmg.json <output directory>

(replace <output directory> with the location where you want the dmg file).