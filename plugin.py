# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

from __future__ import unicode_literals, division, absolute_import, print_function

import os
import sys
import shutil
from time import sleep
from contextlib import contextmanager
from datetime import datetime, timedelta


from compatibility_utils import PY2, unicode_str
from unipath import pathof

import mmth
from utilities import expanduser, file_open
from updatecheck import UpdateChecker
from quickepub import QuickEpub


if PY2:
    from Tkinter import Tk
    import tkFileDialog as tkinter_filedialog
    import tkMessageBox as tkinter_msgbox
else:
    from tkinter import Tk
    import tkinter.filedialog as tkinter_filedialog
    import tkinter.messagebox as tkinter_msgbox


_DEBUG_ = False
prefs = {}
img_map = None

class ImageWriter(object):
    def __init__(self, output_dir):
        global img_map
        img_map = {}
        self._output_dir = output_dir
        self._image_number = 1
        
    def __call__(self, element):
        global img_map
        extension = element.content_type.partition("/")[2]
        image_filename = 'img{0}.{1}'.format(self._image_number, extension)
        with open(os.path.join(self._output_dir, image_filename), 'wb') as image_dest:
            with element.open() as image_source:
                shutil.copyfileobj(image_source, image_dest)
        
        self._image_number += 1
        image_src = '../Images/{0}'.format(image_filename)
        img_map[image_filename] = element.content_type
        return {'src': image_src}


@contextmanager
def make_temp_directory():
    import tempfile
    import shutil
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def fileChooser():
    localRoot = Tk()
    localRoot.withdraw()
    file_opt = {}
    file_opt['parent'] = None
    file_opt['title']= 'Select DOCX file'
    file_opt['defaultextension'] = '.docx'
    # retrieve the initialdir from JSON prefs
    file_opt['initialdir'] = unicode_str(prefs['use_file_path'], 'utf-8')
    file_opt['multiple'] = False
    file_opt['filetypes'] = [('DOCX Files', ('.docx'))]
    localRoot.quit()
    return tkinter_filedialog.askopenfilename(**file_opt)

def update_msgbox(title, msg):
    localRoot = Tk()
    localRoot.withdraw()
    localRoot.option_add('*font', 'Helvetica -12')
    localRoot.quit()
    return tkinter_msgbox.showinfo(title, msg)

def run(bk):
    global prefs
    global img_map
    prefs = bk.getPrefs()

    # set default preference values
    if 'use_file_path' not in prefs:
        prefs['use_file_path'] = expanduser('~')
    if 'epub_version' not in prefs:
        prefs['epub_version'] = '2.0'
    if 'check_for_updates' not in prefs:
        prefs['check_for_updates'] = True
    if 'last_time_checked' not in prefs:
        prefs['last_time_checked'] = str(datetime.now() - timedelta(hours=7))
    if 'last_online_version' not in prefs:
        prefs['last_online_version'] = '0.1.0'

    if prefs['check_for_updates']:
        chk = UpdateChecker(prefs['last_time_checked'], prefs['last_online_version'], bk._w)
        update_available, online_version, time = chk.update_info()
        # update preferences with latest date/time/version
        prefs['last_time_checked'] = time
        if online_version is not None:
            prefs['last_online_version'] = online_version
        if update_available:
            title = 'Plugin Update Available'
            msg = 'Version {} of the {} plugin is now available.'.format(online_version, bk._w.plugin_name)
            update_msgbox(title, msg)

    if _DEBUG_:
        print('Python sys.path', sys.path)

    inpath = fileChooser()
    if inpath == '' or not os.path.exists(inpath):
        print('No input file selected!')
        bk.savePrefs(prefs)
        return 0

    print ('Path to DOCX file {0}'.format(inpath))
    prefs['use_file_path'] = pathof(os.path.dirname(inpath))
    

    with make_temp_directory() as temp_dir:
        epub_build = os.path.join(temp_dir, 'OEBPS')
        os.mkdir(os.path.join(epub_build))
        img_dir = os.path.join(epub_build, 'Images')
        os.mkdir(os.path.join(img_dir))
        convert_image = mmth.images.img_element(ImageWriter(img_dir))
        with open(inpath, 'rb') as docx_file:
            result = mmth.convert_to_html(docx_file, convert_image=convert_image)
            docx_html = result.value
            messages = result.messages
            if _DEBUG_:
                for message in result.messages:
                    print(message)

        htmlfile = os.path.join(epub_build,'Section0001.xhtml')
        file_open(htmlfile,'wb').write(docx_html.encode('utf-8'))
        qe = QuickEpub(temp_dir, epub_build, htmlfile, prefs['epub_version'], img_map)
        epub = qe.makeEPUB()

        # Save prefs to json
        bk.savePrefs(prefs)
        if _DEBUG_:
            print ('Path to epub or src {0}'.format(epub))
        #sleep(30)
        with file_open(epub,'rb')as fp:
            data = fp.read()
        bk.addotherfile('dummy.epub', data)

    return 0

def main():
    print ('I reached main when I should not have\n')
    return -1

if __name__ == "__main__":
    sys.exit(main())
