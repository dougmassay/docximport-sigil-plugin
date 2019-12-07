DOCXImport (A Sigil Plugin)
============

Import DOCX documents into Sigil as epubs

A Sigil plugin based on the Python [Mammoth module](https://github.com/mwilliamson/python-mammoth).

**NOTE: this plugin periodically checks for updated versions by connecting to this Github repository**
(this behavior can be change in the GUI)

Links
=====

* Sigil website is at <http://sigil-ebook.com>
* Sigil support forums are at <http://www.mobileread.com/forums/forumdisplay.php?f=203>
* DOCXImport plugin MobileRead support thread: <http://www.mobileread.com/forums/showthread.php?t=273966>

Building
========

First, clone the repo:

`$git clone https://github.com/dougmassay/docximport-sigil-plugin.git`

To create the plugin zip file, run the buildplugin.py script (root of the repository tree) with Python (Python3-only)

`$python buildplugin` (or just ./buildplugin if Python is in your path)

This will create the DOCXImport_vX.X.X.zip file that can then be installed into Sigil's plugin manager.

`$python buildplugin -l` (or --language) to compile any language files (.ts) and the .qm files to the plugin (Qt's lrelease must be installed and on your PATH for this to work).

Using DOCXImport
=================
If you're using Sigil v0.9.0 or later on OSX or Windows, all dependencies should already be met so long as you're using the bundled Python interpreter (default).

Linux users will have to make sure that the Tk or PyQt5 graphical python module is present if it's not already.  On Debian-based flavors this can be done with "sudo apt-get install python3-tk" (or python3-pyqt5).

* **Note:** Do not rename any Sigil plugin zip files before attempting to install them

This plugin will work with either Python 3.4+.
The absolute minimum version of Sigil required is v0.8.3 (Python must be installed separately prior to v0.9.0)

Get more help at the DOCXImport plugin [MobileRead support thread.](http://www.mobileread.com/forums/showthread.php?t=273966)

A sample docx file (along with a sample mammoth style map and css file) are available in the samples folder of the github reppository. For more help with custom style maps, check out the "Writing Style Maps" section of the [Mammoth README.](https://github.com/mwilliamson/python-mammoth#writing-style-maps)


Contributing / Modifying
============
From here on out, a proficiency with developing / creating Sigil plugins is assumed.
If you need a crash-course, an introduction to creating Sigil plugins is available at
http://www.mobileread.com/forums/showthread.php?t=251452.

The core plugin files (this is where most contributors will spend their time) are:

    > mmth (modified Mammoth module)
    > cbbl (modified Cobble module)
    > images (icon)
    > gui_utilities.py
    > htmlformat.py
    > plugin.py
    > plugin.xml
    > qtdialogs.py
    > quickepub.py
    > tkdialogs.py
    > updatecheck.py

Files used for building/maintaining the plugin:

    > buildplugin  -- this is used to build the plugin.
    > setup.cfg -- used for flake8 style checking. Use it to see if your code complies.
    > checkversion.xml -- used by automatic update checking (not yet implemented).


Feel free to fork the repository and submit pull requests (or just use it privately to experiment).

Would you like to contribute to the translating of DOCXImport? Copy the base.ts file from the translation folder, rename it to 'docximport_(your_locale).ts' (ex. docximport_fr.ts for French) and complete it with Qt's Linguist program. Use a pull requet with the completed ts file added to get it into the official releases.



License Information
=======

### DOCXImport (this plugin)

    Released under the GPLv3.

### [Mammoth](https://github.com/mwilliamson/python-mammoth) - "Convert Word documents to simple and clean HTML"

Released under the 2-Clause BSD License

Copyright (c) 2013, Michael Williamson
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

### [Cobble](https://github.com/mwilliamson/python-cobble) - "Create Python data objects"

Released under the 2-Clause BSD License

Copyright (c) 2013, Michael Williamson
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
