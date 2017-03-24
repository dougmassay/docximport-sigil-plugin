# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

from __future__ import unicode_literals, division, absolute_import, print_function

import sys
import os
import webbrowser
import binascii

from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog, QPushButton, QLabel, QCheckBox, QLineEdit, QGroupBox,
                             QVBoxLayout, QGridLayout, QRadioButton, QSpacerItem, QSizePolicy, QDialogButtonBox, QButtonGroup)
from PyQt5.QtCore import pyqtSlot, QCoreApplication, Qt

from updatecheck import UpdateChecker, DOWNLOAD_PAGE


_DETAILS = {
    'docx'   : None,
    'smap'   : (False, None),
    'css'    : (False, None),
    'vers'   : '2.0',
}


def launch_qt_gui(bk, prefs):
    app = QApplication(sys.argv)
    ex = App(bk, prefs)
    ex.show()
    app.exec_()
    return _DETAILS


# No translation currently taking place, but it doesn't hurt to get a head start.
_translate = QCoreApplication.translate

class App(QWidget):
    def __init__(self, bk, prefs):
        super().__init__()

        self.bk = bk
        self.prefs = prefs
        self.update = False
        self._ok_to_close = False

        self.FTYPE_MAP = {
            'smap': {
                'title'            : _translate('App', 'Select custom style-map file'),
                'defaultextension' : '.txt',
                'filetypes'        : 'Text Files (*.txt);;All files (*.*)',
                },
            'css' : {
                'title'            : _translate('App', 'Select custom CSS file'),
                'defaultextension' : '.css',
                'filetypes'        : 'CSS Files (*.css)',
                },
            'docx' : {
                'title'            : _translate('App', 'Select DOCX file'),
                'defaultextension' : '.docx',
                'filetypes'        : 'DOCX Files (*.docx)',
                },
        }

        # Check online github files for newer version
        if self.prefs['check_for_updates']:
            self.update, self.newversion = self.check_for_update()
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout(self)

        self.upd_layout = QVBoxLayout()
        self.update_label = QLabel()
        self.update_label.setAlignment(Qt.AlignCenter)
        self.upd_layout.addWidget(self.update_label)
        self.get_update_button = QPushButton()
        self.get_update_button.clicked.connect(self.get_update)
        self.upd_layout.addWidget(self.get_update_button)
        main_layout.addLayout(self.upd_layout)
        if not self.update:
            self.update_label.hide()
            self.get_update_button.hide()

        self.details_grid = QGridLayout()
        self.epub2_select = QRadioButton()
        self.epub2_select.setText('EPUB2')
        self.epubType = QButtonGroup()
        self.epubType.addButton(self.epub2_select)
        self.details_grid.addWidget(self.epub2_select, 0, 0, 1, 1)
        self.checkbox_get_updates = QCheckBox()
        self.details_grid.addWidget(self.checkbox_get_updates, 0, 1, 1, 1)
        self.epub3_select = QRadioButton()
        self.epub3_select.setText('EPUB3')
        self.epubType.addButton(self.epub3_select)
        self.details_grid.addWidget(self.epub3_select, 1, 0, 1, 1)
        main_layout.addLayout(self.details_grid)
        self.checkbox_get_updates.setChecked(self.prefs['check_for_updates'])
        if self.prefs['epub_version'] == '2.0':
            self.epub2_select.setChecked(True)
        elif self.prefs['epub_version'] == '3.0':
            self.epub3_select.setChecked(True)
        else:
            self.epub2_select.setChecked(True)

        self.groupBox = QGroupBox()
        self.groupBox.setTitle('')
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.docx_grid = QGridLayout()
        self.docx_label = QLabel()
        self.docx_grid.addWidget(self.docx_label, 0, 0, 1, 1)
        self.docx_path = QLineEdit()
        self.docx_grid.addWidget(self.docx_path, 1, 0, 1, 1)
        self.choose_docx_button = QPushButton()
        self.choose_docx_button.setText('...')
        self.docx_grid.addWidget(self.choose_docx_button, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.docx_grid)
        self.choose_docx_button.clicked.connect(lambda: self.fileChooser('docx', self.docx_path))
        if len(self.prefs['lastDocxPath']):
            self.docx_path.setText(self.prefs['lastDocxPath'])
        self.docx_path.setEnabled(False)

        self.smap_grid = QGridLayout()
        self.checkbox_smap = QCheckBox(self.groupBox)
        self.smap_grid.addWidget(self.checkbox_smap, 0, 0, 1, 1)
        self.cust_smap_path = QLineEdit(self.groupBox)
        self.smap_grid.addWidget(self.cust_smap_path, 1, 0, 1, 1)
        self.choose_smap_button = QPushButton(self.groupBox)
        self.choose_smap_button.setText('...')
        self.smap_grid.addWidget(self.choose_smap_button, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.smap_grid)
        self.checkbox_smap.setChecked(self.prefs['useSmap'])
        self.checkbox_smap.stateChanged.connect(lambda: self.chkBoxActions(self.checkbox_smap, self.choose_smap_button))
        self.choose_smap_button.clicked.connect(lambda: self.fileChooser('smap', self.cust_smap_path, self.checkbox_smap, self.choose_smap_button))
        if len(self.prefs['useSmapPath']):
            self.cust_smap_path.setText(self.prefs['useSmapPath'])
        self.cust_smap_path.setEnabled(False)
        self.chkBoxActions(self.checkbox_smap, self.choose_smap_button)

        self.css_grid = QGridLayout()
        self.checkbox_css = QCheckBox(self.groupBox)
        self.css_grid.addWidget(self.checkbox_css, 0, 0, 1, 1)
        self.cust_css_path = QLineEdit(self.groupBox)
        self.css_grid.addWidget(self.cust_css_path, 1, 0, 1, 1)
        self.choose_css_button = QPushButton(self.groupBox)
        self.choose_css_button.setText('...')
        self.css_grid.addWidget(self.choose_css_button, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.css_grid)
        self.checkbox_css.setChecked(self.prefs['useCss'])
        self.checkbox_css.stateChanged.connect(lambda: self.chkBoxActions(self.checkbox_css, self.choose_css_button))
        self.choose_css_button.clicked.connect(lambda: self.fileChooser('css', self.cust_css_path, self.checkbox_css, self.choose_css_button))
        if len(self.prefs['useCssPath']):
            self.cust_css_path.setText(self.prefs['useCssPath'])
        self.cust_css_path.setEnabled(False)
        self.chkBoxActions(self.checkbox_css, self.choose_css_button)

        main_layout.addWidget(self.groupBox)
        self.checkbox_debug = QCheckBox()
        main_layout.addWidget(self.checkbox_debug)
        self.checkbox_debug.setChecked(self.prefs['debug'])

        spacerItem = QSpacerItem(20, 15, QSizePolicy.Minimum, QSizePolicy.Expanding)
        main_layout.addItem(spacerItem)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self._ok_clicked)
        button_box.rejected.connect(self._cancel_clicked)
        main_layout.addWidget(button_box)
        self.retranslateUi(self)
        if self.prefs['qt_geometry'] is not None:
            self.restoreGeometry(binascii.a2b_base64(self.prefs['qt_geometry'].encode('ascii')))
        self.show()

    def retranslateUi(self, App):
        # No translation currently taking place, but it doesn't hurt to get a head start.
        self.setWindowTitle(_translate('App', 'DOCXImport'))
        self.update_label.setText(_translate('App', 'Plugin Update Available'))
        self.get_update_button.setText(_translate('App', 'Go to download page'))
        self.checkbox_get_updates.setText(_translate('App', 'Check for plugin updates'))
        self.docx_label.setText(_translate('App', 'DOCX File to import'))
        self.checkbox_smap.setText(_translate('App', 'Use Custom Style Map'))
        self.checkbox_css.setText(_translate('App', 'Use Custom CSS'))
        self.checkbox_debug.setText(_translate('App', 'Debug Mode (change takes effect next plugin run)'))

    def fileChooser(self, ftype, qlineedit, qcheck=None, qbutton=None):
        _translate = QCoreApplication.translate
        options =  QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        title = self.FTYPE_MAP[ftype]['title']
        startfolder = self.prefs['lastDir'][ftype]
        ffilter = self.FTYPE_MAP[ftype]['filetypes']
        inpath, _ = QFileDialog.getOpenFileName(self, _translate('APP', title), startfolder, ffilter, options=options)
        if len(inpath):
            qlineedit.setEnabled(True)
            qlineedit.setText(os.path.normpath(inpath))
            self.prefs['lastDir'][ftype] = os.path.dirname(inpath)
            qlineedit.setEnabled(False)
        else:
            if qcheck is not None:
                qcheck.setChecked(False)
            if qbutton is not None:
                qbutton.setEnabled(False)

    def chkBoxActions(self, chk, btn):
        btn.setEnabled(chk.isChecked())

    def cmdDo(self):
        global _DETAILS
        self.prefs['qt_geometry'] = binascii.b2a_base64(self.saveGeometry()).decode('ascii')
        self.prefs['check_for_updates'] = self.checkbox_get_updates.isChecked()
        self.prefs['epub_version'] = self.epubType.checkedButton().text()[-1] + '.0'
        self.prefs['debug'] = self.checkbox_debug.isChecked()
        _DETAILS['vers'] = self.epubType.checkedButton().text()[-1] + '.0'
        self.prefs['useSmap'] = self.checkbox_smap.isChecked()
        if self.checkbox_smap.isChecked():
            if len(self.cust_smap_path.text()):
                self.prefs['useSmapPath'] = self.cust_smap_path.text()
                _DETAILS['smap'] = (self.checkbox_smap.isChecked(), self.cust_smap_path.text())
            else:
                # Message box that no file is selected
                return
        self.prefs['useCss'] = self.checkbox_css.isChecked()
        if self.checkbox_css.isChecked():
            if len(self.cust_css_path.text()):
                self.prefs['useCssPath'] = self.cust_css_path.text()
                _DETAILS['css'] = (self.checkbox_css.isChecked(), self.cust_css_path.text())
            else:
                # Message box that no file is selected
                return
        if len(self.docx_path.text()):
            self.prefs['lastDocxPath'] = self.docx_path.text()
            _DETAILS['docx'] = self.docx_path.text()
        else:
            # Message box that no file is selected
            return

    def check_for_update(self):
        '''Use updatecheck.py to check for newer versions of the plugin'''
        chk = UpdateChecker(self.prefs['last_time_checked'], self.bk._w)
        update_available, online_version, time = chk.update_info()
        # update preferences with latest date/time/version
        self.prefs['last_time_checked'] = time
        if online_version is not None:
            self.prefs['last_online_version'] = online_version
        if update_available:
            return (True, online_version)
        return (False, online_version)

    def get_update(self):
        url = DOWNLOAD_PAGE
        if self.update:
            latest = '/tag/v{}'.format(self.newversion)
            url = url + latest
        webbrowser.open_new_tab(url)

    @pyqtSlot()
    def _ok_clicked(self):
        self._ok_to_close = True
        self.cmdDo()
        self.bk.savePrefs(self.prefs)
        QCoreApplication.instance().quit()

    @pyqtSlot()
    def _cancel_clicked(self):
        self._ok_to_close = True
        '''Close aborting any changes'''
        self.prefs['qt_geometry'] = binascii.b2a_base64(self.saveGeometry()).decode('ascii')
        self.prefs['check_for_updates'] = self.checkbox_get_updates.isChecked()
        self.prefs['debug'] = self.checkbox_debug.isChecked()
        self.bk.savePrefs(self.prefs)
        QCoreApplication.instance().quit()

    def closeEvent(self, event):
        if self._ok_to_close:
            event.accept()  # let the window close
        else:
            self._cancel_clicked()

def main():
    ''' For debugging the qt dialog outside of the sigil plugin '''
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

    prefs['language'] = 'en'
    prefs['qt_geometry'] = None
    prefs['use_file_path'] = os.path.expanduser('~')
    prefs['epub_version'] = '3.0'
    prefs['check_for_updates'] = False
    prefs['last_time_checked'] = str(datetime.now() - timedelta(hours=13))
    prefs['last_online_version'] = '0.1.0'
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

    details = launch_qt_gui(sim_bk, prefs)
    print(details)
    return 0


if __name__ == "__main__":
    sys.exit(main())
