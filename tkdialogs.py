# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

from __future__ import unicode_literals, division, absolute_import, print_function

import sys
import os
import webbrowser

import tkinter
from tkinter.filedialog import askopenfilename

from updatecheck import UpdateChecker, DOWNLOAD_PAGE


FTYPE_MAP = {
    'smap': {
        'title'            : 'Select custom style-map file',
        'defaultextension' : '.txt',
        'filetypes'        : [('Text Files', '.txt'), ('All files', '.*')],
        },
    'css' : {
        'title'            : 'Select custom CSS file',
        'defaultextension' : '.css',
        'filetypes'        : [('CSS Files', '.css')]
        },
    'docx' : {
        'title'            : 'Select DOCX file',
        'defaultextension' : '.docx',
        'filetypes'        : [('DOCX Files', '.docx')]
        },
}

_DETAILS = {
    'docx'   : None,
    'smap'   : (False, None),
    'css'    : (False, None),
    'vers'   : '2.0',
}


def launch_tk_gui(bk, prefs):
    root = tkinter.Tk()
    root.withdraw()
    root.title('')
    root.resizable(True, True)
    root.minsize(420, 400)
    root.option_add('*font', 'Arial -12')
    if not sys.platform.startswith('darwin'):
        img = tkinter.Image('photo', file=os.path.join(bk._w.plugin_dir, bk._w.plugin_name, 'images/icon.png'))
        root.tk.call('wm','iconphoto',root._w,img)
    guiMain(root, bk, prefs).pack(fill=tkinter.constants.BOTH, expand=True)
    root.mainloop()
    return _DETAILS

class guiMain(tkinter.Frame):
    def __init__(self, parent, bk, prefs):
        tkinter.Frame.__init__(self, parent, border=5)
        self.parent = parent
        # Edit Plugin container object
        self.bk = bk
        self.prefs = prefs
        self.update = False

        # Check online github files for newer version
        if self.prefs['check_for_updates']:
            self.update, self.newversion = self.check_for_update()

        if self.prefs['windowGeometry'] is None:
            # Sane geometry defaults
            self.parent.update_idletasks()
            w = self.parent.winfo_screenwidth()
            h = self.parent.winfo_screenheight()
            rootsize = (420, 400)
            x = w/2 - rootsize[0]/2
            y = h/2 - rootsize[1]/2
            self.prefs['windowGeometry'] = ('%dx%d+%d+%d' % (rootsize + (x, y)))

        self.initUI()
        parent.protocol('WM_DELETE_WINDOW', self.quitApp)

    def initUI(self):
        ''' Build the GUI and assign variables and handler functions to elements. '''
        self.parent.title(self.bk._w.plugin_name)
        body = tkinter.Frame(self)

        update_label = tkinter.Label(body, text='Plugin Update Available', fg='red')
        update_label.pack(side=tkinter.constants.TOP, fill=tkinter.constants.BOTH)
        get_update_button = tkinter.Button(body, text='Go to download page', command=self.get_update)
        get_update_button.pack(side=tkinter.constants.TOP, fill=tkinter.constants.BOTH)

        chk_frame_updates = tkinter.Frame(body, pady=10)
        self.epubType = tkinter.StringVar()
        radio_frame_etype = tkinter.Frame(chk_frame_updates)
        radio_epub2_select = tkinter.Radiobutton(radio_frame_etype, text='EPUB2', var=self.epubType, value='2.0')
        radio_epub2_select.pack(side=tkinter.constants.TOP)
        radio_epub3_select = tkinter.Radiobutton(radio_frame_etype, text='EPUB3', var=self.epubType, value='3.0')
        radio_epub3_select.pack(side=tkinter.constants.TOP)
        radio_frame_etype.pack(side=tkinter.constants.LEFT)
        if self.prefs['epub_version'] == '2.0':
            radio_epub2_select.select()
        elif self.prefs['epub_version'] == '3.0':
            radio_epub3_select.select()
        else:
            radio_epub2_select.select()
        self.use_updates = tkinter.BooleanVar()
        checkbox_get_updates = tkinter.Checkbutton(chk_frame_updates, text='Check for plugin updates', variable=self.use_updates)
        checkbox_get_updates.pack(side=tkinter.constants.RIGHT, anchor=tkinter.constants.N)
        chk_frame_updates.pack(side=tkinter.constants.TOP, fill=tkinter.constants.BOTH)
        if self.prefs['check_for_updates']:
            checkbox_get_updates.select()
        if not self.update:
            update_label.pack_forget()
            get_update_button.pack_forget()

        entry_frame_docxpath = tkinter.Frame(body)
        dash_label = tkinter.Label(entry_frame_docxpath, text='DOCX File to import', pady=3)
        dash_label.pack(fill=tkinter.constants.BOTH)
        self.docx_path = tkinter.Entry(entry_frame_docxpath)
        self.docx_path.pack(side=tkinter.constants.LEFT, fill=tkinter.constants.BOTH, expand=1)
        self.choose_docx_button = tkinter.Button(entry_frame_docxpath, text='...', command=lambda: self.fileChooser('docx', self.docx_path))
        self.choose_docx_button.pack(side=tkinter.constants.RIGHT, fill=tkinter.constants.BOTH)
        if len(self.prefs['lastDocxPath']):
            self.docx_path.insert(0, self.prefs['lastDocxPath'])
        self.docx_path.config(state='readonly')
        entry_frame_docxpath.pack(side=tkinter.constants.TOP, fill=tkinter.constants.BOTH)

        tkinter.Label(body, pady=3).pack()

        main_frame = tkinter.Frame(body, bd=1, relief=tkinter.constants.GROOVE)
        chk_frame_smap = tkinter.Frame(main_frame)
        self.use_smap = tkinter.BooleanVar()
        self.checkbox_smap = tkinter.Checkbutton(chk_frame_smap, pady=3, text='Use custom style map', command=self.chkBoxActions, variable=self.use_smap)
        self.checkbox_smap.pack(side=tkinter.constants.LEFT, fill=tkinter.constants.BOTH)
        chk_frame_smap.pack(side=tkinter.constants.TOP, fill=tkinter.constants.BOTH)
        if self.prefs['useSmap']:
            self.checkbox_smap.select()

        entry_frame_smappath = tkinter.Frame(main_frame)
        self.cust_smap_path = tkinter.Entry(entry_frame_smappath)
        self.cust_smap_path.pack(side=tkinter.constants.LEFT, fill=tkinter.constants.BOTH, expand=1)
        self.choose_smap_button = tkinter.Button(entry_frame_smappath, text='...',
                                                 command=lambda: self.fileChooser('smap', self.cust_smap_path, self.checkbox_smap, self.choose_smap_button))
        self.choose_smap_button.pack(side=tkinter.constants.RIGHT, fill=tkinter.constants.BOTH)
        if len(self.prefs['useSmapPath']):
            self.cust_smap_path.insert(0, self.prefs['useSmapPath'])
        self.cust_smap_path.config(state='readonly')
        if not self.use_smap.get():
            self.choose_smap_button.config(state='disabled')
        entry_frame_smappath.pack(side=tkinter.constants.TOP, fill=tkinter.constants.BOTH)

        chk_frame_css = tkinter.Frame(main_frame)
        self.use_css = tkinter.BooleanVar()
        self.checkbox_css = tkinter.Checkbutton(chk_frame_css, pady=3, text='Use custom css', command=self.chkBoxActions, variable=self.use_css)
        self.checkbox_css.pack(side=tkinter.constants.LEFT, fill=tkinter.constants.BOTH)
        chk_frame_css.pack(side=tkinter.constants.TOP, fill=tkinter.constants.BOTH)
        if self.prefs['useCss']:
            self.checkbox_css.select()

        entry_frame_csspath = tkinter.Frame(main_frame)
        self.cust_css_path = tkinter.Entry(entry_frame_csspath)
        self.cust_css_path.pack(side=tkinter.constants.LEFT, fill=tkinter.constants.BOTH, expand=1)
        self.choose_css_button = tkinter.Button(entry_frame_csspath, text='...',
                                                command=lambda: self.fileChooser('css', self.cust_css_path, self.checkbox_css, self.choose_css_button))
        self.choose_css_button.pack(side=tkinter.constants.RIGHT, fill=tkinter.constants.BOTH)
        if len(self.prefs['useCssPath']):
            self.cust_css_path.insert(0, self.prefs['useCssPath'])
        self.cust_css_path.config(state='readonly')
        if not self.use_css.get():
            self.choose_css_button.config(state='disabled')
        entry_frame_csspath.pack(side=tkinter.constants.TOP, fill=tkinter.constants.BOTH)

        self.debug = tkinter.BooleanVar()
        checkbox_debug = tkinter.Checkbutton(body, text='Debug Mode (change takes effect next plugin run)', variable=self.debug)
        checkbox_debug.pack(side=tkinter.constants.BOTTOM, pady=10, anchor=tkinter.constants.W)
        if self.prefs['debug']:
            checkbox_debug.select()

        main_frame.pack(side=tkinter.constants.TOP, fill=tkinter.constants.BOTH)

        # Dialog buttonbox (three buttons)
        buttons = tkinter.Frame()
        self.gbutton = tkinter.Button(buttons, text='Apply and Close', command=self.cmdDo)
        self.gbutton.pack(side=tkinter.constants.LEFT, fill=tkinter.constants.BOTH, expand=True)
        self.qbutton = tkinter.Button(buttons, text='Cancel', command=self.cmdCancel)
        self.qbutton.pack(side=tkinter.constants.LEFT, fill=tkinter.constants.BOTH, expand=True)
        buttons.pack(side=tkinter.constants.BOTTOM, pady=5, padx=5, fill=tkinter.constants.BOTH)

        body.pack(fill=tkinter.constants.BOTH)

        # Get the saved window geometry settings
        self.parent.geometry(self.prefs['windowGeometry'])
        self.parent.deiconify()
        self.parent.lift()

    def chkBoxActions(self):
        if self.use_smap.get():
            self.choose_smap_button.config(state='normal')
        else:
            self.choose_smap_button.config(state='disabled')

        if self.use_css.get():
            self.choose_css_button.config(state='normal')
        else:
            self.choose_css_button.config(state='disabled')

    def fileChooser(self, ftype, tkentry, tkcheck=None, tkbutton=None):
        file_opt = FTYPE_MAP[ftype]
        file_opt['parent'] = None
        file_opt['initialdir'] = self.prefs['lastDir'][ftype]
        file_opt['multiple'] = False
        inpath = askopenfilename(**file_opt)
        if len(inpath):
            tkentry.config(state="normal")
            tkentry.delete(0, tkinter.constants.END)
            tkentry.insert(0, os.path.normpath(inpath))
            self.prefs['lastDir'][ftype] = os.path.dirname(inpath)
            tkentry.config(state="readonly")
        else:
            if tkcheck is not None:
                tkcheck.deselect()
            if tkbutton is not None:
                tkbutton.config(state='disabled')

    def cmdDo(self):
        global _DETAILS
        self.prefs['windowGeometry'] = self.parent.geometry()
        self.prefs['check_for_updates'] = self.use_updates.get()
        self.prefs['epub_version'] = self.epubType.get()
        self.prefs['debug'] = self.debug.get()
        _DETAILS['vers'] = self.epubType.get()
        self.prefs['useSmap'] = self.use_smap.get()
        if self.use_smap.get():
            if len(self.cust_smap_path.get()):
                self.prefs['useSmapPath'] = self.cust_smap_path.get()
                _DETAILS['smap'] = (self.use_smap.get(), self.cust_smap_path.get())
            else:
                # Message box that no file is selected
                return
        self.prefs['useCss'] = self.use_css.get()
        if self.use_css.get():
            if len(self.cust_css_path.get()):
                self.prefs['useCssPath'] = self.cust_css_path.get()
                _DETAILS['css'] = (self.use_css.get(), self.cust_css_path.get())
            else:
                # Message box that no file is selected
                return
        if len(self.docx_path.get()):
            self.prefs['lastDocxPath'] = self.docx_path.get()
            _DETAILS['docx'] = self.docx_path.get()
        else:
            # Message box that no file is selected
            return
        self.bk.savePrefs(self.prefs)
        self.quitApp()

    def cmdCancel(self):
        '''Close aborting any changes'''
        self.prefs['windowGeometry'] = self.parent.geometry()
        self.prefs['check_for_updates'] = self.use_updates.get()
        self.prefs['debug'] = self.debug.get()
        self.bk.savePrefs(self.prefs)
        self.quitApp()

    def quitApp(self):
        '''Clean up and close Widget'''
        try:
            self.parent.destroy()
            self.parent.quit()
        except:
            pass

    def check_for_update(self):
        '''Use updatecheck.py to check for newer versions of the plugin'''
        chk = UpdateChecker(self.prefs['last_time_checked'], self.bk._w)
        print(self.prefs['last_time_checked'])
        update_available, online_version, time = chk.update_info()
        # update preferences with latest date/time/version
        self.prefs['last_time_checked'] = time
        if online_version is not None:
            self.prefs['last_online_version'] = online_version
        print(update_available, online_version)
        if update_available:
            return (True, online_version)
        return (False, online_version)

    def get_update(self):
        url = DOWNLOAD_PAGE
        if self.update:
            latest = '/tag/v{}'.format(self.newversion)
            url = url + latest
        webbrowser.open_new_tab(url)


def main():
    ''' For debugging the tkinter dialog outside of the sigil plugin '''
    from datetime import datetime, timedelta
    prefs = {}

    # Fake book container object
    class w(object):
        def __init__(self):
            w.plugin_name = 'DOCXImport'
            w.plugin_dir = '/home/dlmassay/.local/share/sigil-ebook/sigil/plugins'

    class bk(object):
        def __init__(self):
            bk._w = w()

        def savePrefs(self, dummy):
            return
    sim_bk = bk()

    prefs['use_file_path'] = os.path.expanduser('~')
    prefs['epub_version'] = '2.0'
    prefs['check_for_updates'] = True
    prefs['last_time_checked'] = str(datetime.now() - timedelta(days=3))
    prefs['last_online_version'] = '0.1.0'
    prefs['windowGeometry'] = None
    prefs['lastDir'] = {
        'smap' : os.path.expanduser('~'),
        'css'  : os.path.expanduser('~'),
        'docx' : os.path.expanduser('~'),
    }
    prefs['useSmap'] = False
    prefs['useSmapPath'] = ''
    prefs['useCss'] = False
    prefs['useCssPath'] = ''
    prefs['lastDocxPath'] = ''
    prefs['debug'] = False

    details = launch_tk_gui(sim_bk, prefs)
    print(details)
    return 0


if __name__ == "__main__":
    sys.exit(main())
