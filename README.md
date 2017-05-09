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

    $ git clone https://github.com/dougmassay/docximport-sigil-plugin.git

To create the plugin zip file, run the buildplugin.py script (root of the repository tree) with Python (2 or 3)

    $python buildplugin (or just ./buildplugin if Python is in your path)

This will create the DOCXImport_vX.X.X.zip file that can then be installed into Sigil's plugin manager.

Using DOCXImport
=================
If you're using Sigil v0.9.0 or later on OSX or Windows, all dependencies should already be met so long as you're using the bundled Python interpreter (default).

Linux users will have to make sure that the Tk or PyQt5 graphical python module is present if it's not already.  On Debian-based flavors this can be done with "sudo apt-get install python3-tk" (or python3-pyqt5).

* **Note:** Do not rename any Sigil plugin zip files before attempting to install them

This plugin will work with either Python 3.4+ or Python 2.7+ (defaults to 3.x if both are present).
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
    > parsim (modified Parsimonious module)
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

### [Parsimonious](https://github.com/erikrose/parsimonious) - "The fastest pure-Python PEG parser I can muster"

Released under the terms of the [MIT license](http://opensource.org/licenses/mit-license.php)

Copyright (c) 2012 Erik Rose

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
