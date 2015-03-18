
Mochitest Tools

This script is designed to work with Mozilla mochitest infrastructure. 
It was created to remove excludetests from b2g.json, b2g-debug.json, b2g-desktop.json and add skip-ifs to mochitest.ini files.

Usage

    1) Download Firefox build.
    2) Clone mochitest-tools repository
    3) Edit the filename of js1, js2, js3 variables to put your local path in b2geditor.py
    4) Edit outfile1, outfile2, outfile3 to put your local path in b2geditor.py
    5) Run b2geditor.py and view the results
If everything is proper, skip-ifs will be added to mochitest.ini files for corresponding entries in b2g.json, b2g-debug.json, b2g-desktop.json

Limitations

This script will only remove those entries of excludetests from b2g.json, b2g-debug.json and b2g-desktop.json that have a mochitest.ini file located in the particular directory. 
It will leave other entries as it is in the respective .json directory.
