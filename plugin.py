# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

from __future__ import unicode_literals, division, absolute_import, print_function

import os
import sys
import io
import shutil
import tempfile
import subprocess
from contextlib import contextmanager
from datetime import datetime, timedelta

import mmth
from quickepub import QuickEpub
from htmlformat import build_html


_DEBUG_ = False

_wmf_mimetypes = ["image/x-wmf", "image/x-emf"]

_img_extensions = {
    "image/gif"     : "gif",
    "image/jpeg"    : "jpg",
    "image/png"     : "png",
    "image/svg+xml" : "svg",
    "image/x-wmf"   : "wmf",
    "image/x-emf"   : "emf"
}

prefs = {}
img_map = None

def wmf_prereqs_met():
    return (prefs['libreOfficePath'] != '' and prefs['imageMagickPath'] != '')


class ImageWriter(object):
    def __init__(self, output_dir):
        global img_map
        global prefs
        img_map = {}
        self._output_dir = output_dir
        self._image_number = 1

    def __call__(self, element):
        global img_map
        print("processing an image")
        if element.content_type in _img_extensions:
            extension = _img_extensions.get(element.content_type)
        else:
            extension = element.content_type.partition("/")[2]
        image_filename = original_filename = 'img{0}.{1}'.format(self._image_number, extension)
        if _DEBUG_:
            print('Processing {}'.format(image_filename))

        if prefs['convertWMF'] == True and wmf_prereqs_met() and element.content_type in _wmf_mimetypes:
            image_filename = 'img{0}.png'.format(self._image_number)

            try:
                image = libreoffice_wmf_conversion(element, post_process=imagemagick_trim)
            except:
                image = element
                image_filename = original_filename
        else:
            image = element
                
        with open(os.path.join(self._output_dir, image_filename), 'wb') as image_dest:
            with image.open() as image_source:
                shutil.copyfileobj(image_source, image_dest)

        self._image_number += 1
        image_src = '../Images/{0}'.format(image_filename)
        img_map[image_filename] = image.content_type
        return {'src': image_src}

@contextmanager
def make_temp_directory():
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)

def libreoffice_wmf_conversion(image, post_process=None):
    if post_process is None:
        post_process = lambda x: x
    
    wmf_extension = _img_extensions.get(image.content_type)
    temporary_directory = tempfile.mkdtemp()
    try:
        input_path = os.path.join(temporary_directory, "image." + wmf_extension)
        with io.open(input_path, "wb") as input_fileobj:
            with image.open() as image_fileobj:
                shutil.copyfileobj(image_fileobj, input_fileobj)
        
        output_path = os.path.join(temporary_directory, "image.png")
        #libreoffice = "libreoffice"
        #if sys.platform.startswith('win'):
        #    libreoffice = "soffice.exe"
        subprocess.check_call([
            prefs['libreOfficePath'],
            "--headless",
            "--convert-to",
            "png",
            input_path,
            "--outdir",
            temporary_directory,
        ])
        
        with io.open(output_path, "rb") as output_fileobj:
            output = output_fileobj.read()
        
        def open_image():
            return io.BytesIO(output)
        
        return post_process(image.copy(
            content_type="image/png",
            open=open_image,
        ))
    finally:
        shutil.rmtree(temporary_directory)

def imagemagick_trim(image):
    '''
    if sys.platform.startswith('win'):
        exe = "convert.exe"
        if prefs['imageMagickPath'] != '':
            exe = os.path.join(prefs['imageMagickPath'], "convert.exe")
        command = [exe, "-", "-trim", "-"]
    else:
    '''
    command = [prefs['imageMagickPath'], "-", "-trim", "-"]
    process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    try:
        with image.open() as image_fileobj:
            shutil.copyfileobj(image_fileobj, process.stdin)
        output, err_output = process.communicate()
    except:
        process.kill()
        process.wait()
        raise
        
    return_code = process.poll()
    if return_code:
        raise subprocess.CalledProcessError(return_code, command)
    else:
        def open_image():
            return io.BytesIO(output)
        
        return image.copy(open=open_image)


def run(bk):
    global prefs
    global img_map
    global _DEBUG_

    # Use Qt interface if Sigil >= v0.9.8 and/or PyQt5 is available
    supports_pyqt = (bk.launcher_version() >= 20170115)
    if supports_pyqt:
        try:
            from qtdialogs import launch_qt_gui as launch_gui
        except ImportError:  # Using an external python that doeesn't have PyQt5
            from tkdialogs import launch_tk_gui as launch_gui
        else:
            from qtdialogs import launch_qt_gui as launch_gui
    else:
        from tkdialogs import launch_tk_gui as launch_gui

    prefs = bk.getPrefs()

    # set default preference values
    if 'use_file_path' not in prefs:
        prefs['use_file_path'] = os.path.expanduser('~')
    if 'epub_version' not in prefs:
        prefs['epub_version'] = '2.0'
    if 'check_for_updates' not in prefs:
        prefs['check_for_updates'] = True
    if 'last_time_checked' not in prefs:
        prefs['last_time_checked'] = str(datetime.now() - timedelta(hours=7))
    if 'last_online_version' not in prefs:
        prefs['last_online_version'] = '0.1.0'

    if 'windowGeometry' not in prefs:
        prefs['windowGeometry'] = None
    if 'qt_geometry' not in prefs:
        prefs['qt_geometry'] = None
    if 'lastDir' not in prefs:
        prefs['lastDir'] = {
            'smap' : os.path.expanduser('~'),
            'css'  : os.path.expanduser('~'),
            'docx' : os.path.expanduser('~'),
        }
    if 'useSmap' not in prefs:
        prefs['useSmap'] = False
    if 'useSmapPath' not in prefs:
        prefs['useSmapPath'] = ''
    if 'useCss' not in prefs:
        prefs['useCss'] = False
    if 'useCssPath' not in prefs:
        prefs['useCssPath'] = ''
    if 'libreOfficePath' not in prefs:
        cmd = 'libreoffice'
        if sys.platform.startswith('win') or sys.platform.startswith('darwin'):
            cmd = 'soffice'
            if sys.platform.startswith('win'):
                cmd = '{}.exe'.format(cmd)
        tmppath = shutil.which(cmd)
        if tmppath is not None:
            prefs['libreOfficePath'] = tmppath
        else:
            prefs['libreOfficePath'] = ''
    if 'imageMagickPath' not in prefs:
        cmd = 'convert'
        if sys.platform.startswith('win'):
            cmd = '{}.exe'.format(cmd)
        tmppath = shutil.which(cmd)
        if tmppath is not None:
            prefs['imageMagickPath'] = tmppath
        else:
            prefs['imageMagickPath'] = ''
    if 'lastDocxPath' not in prefs:
        prefs['lastDocxPath'] = ''
    if 'debug' not in prefs:
        prefs['debug'] = False
    if 'convertWMF' not in prefs:
        #prefs['convertWMF'] = (prefs['libreOfficePath'] != '' and prefs['imageMagickPath'] != '')
        prefs['convertWMF'] = wmf_prereqs_met()

    _DEBUG_ = prefs['debug']

    if _DEBUG_:
        print('Current Python sys.path: {}.\n'.format(sys.path))

    ''' Launch Main Dialog '''
    details = launch_gui(bk, prefs)
    if _DEBUG_:
        print('Plugin criteria: {}.\n'.format(details))

    inpath = ''
    smap = ''
    if details['docx'] is not None:
        inpath = details['docx']
    if details['smap'][0] and os.path.isfile(details['smap'][1]):
        smap = open(details['smap'][1], encoding='utf-8').read()
        if _DEBUG_:
            print('Custom style map file: {}.\n'.format(details['smap'][1]))
    css = None
    if details['css'][0] and os.path.isfile(details['css'][1]):
        css = open(details['css'][1], encoding='utf-8').read()
        if _DEBUG_:
            print('Custom css file: {}.\n'.format(details['css'][1]))

    if inpath == '' or not os.path.exists(inpath):
        print('No input file selected!')
        return 0

    print('Path to DOCX file {0}.\n'.format(inpath))

    with make_temp_directory() as temp_dir:
        epub_build = os.path.join(temp_dir, 'OEBPS')
        os.mkdir(os.path.join(epub_build))
        img_dir = os.path.join(epub_build, 'Images')
        os.mkdir(os.path.join(img_dir))
        cssfile = None
        if css is not None:
            print('Adding styleheet to epub...\n')
            styles_dir = os.path.join(epub_build, 'Styles')
            os.mkdir(os.path.join(styles_dir))
            cssfile = os.path.join(epub_build,'stylesheet.css')
            open(cssfile,'wb').write(css.encode('utf-8'))

        # Process images (if any)
        convert_image = mmth.images.img_element(ImageWriter(img_dir))

        with open(inpath, 'rb') as docx_file:
            print('Creating html...\n')
            if details['smap'] and len(smap):
                result = mmth.convert_to_html(docx_file, style_map=smap, convert_image=convert_image, ignore_empty_paragraphs=False)
            else:
                result = mmth.convert_to_html(docx_file, convert_image=convert_image, ignore_empty_paragraphs=False)
            docx_html = result.value
            print('Warnings/errors from Mammoth conversion:')
            for message in result.messages:
                print(message)
            print('\n')

        finished_html = build_html(docx_html, details['css'][0])

        print('Adding html file to epub...\n')
        htmlfile = os.path.join(epub_build,'Section0001.xhtml')
        open(htmlfile,'wb').write(finished_html.encode('utf-8'))

        print('Importing epub...\n')
        qe = QuickEpub(temp_dir, epub_build, htmlfile, details['vers'], img_map, cssfile)
        epub = qe.makeEPUB()

        if _DEBUG_:
            print('Path to epub or src {0}.\n'.format(epub))
        # sleep(30)
        with open(epub,'rb')as fp:
            data = fp.read()
        bk.addotherfile('dummy.epub', data)

    return 0

def main():
    print('I reached main when I should not have\n')
    return -1


if __name__ == "__main__":
    sys.exit(main())
