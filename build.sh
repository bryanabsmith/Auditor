#!/usr/bin/env bash

echo "\e[31m:: Freezing Auditor...\e[0m"
python setup.py bdist_mac

echo "\e[31m:: Moving app bundle...\e[0m"
mv build/*.app ./Auditor.app/

echo "\e[31m:: Setting icon...\e[0m"
/Applications/Xcode.app/Contents/Developer/Tools/DeRez -only icns Auditor.icns > Auditor.rsrc


echo "\e[31m:: Building installation disk image...\e[0m"
appdmg appdmg.json ~/Desktop/auditor.dmg

