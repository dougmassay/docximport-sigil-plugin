# -*- coding: utf-8 -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab

from __future__ import unicode_literals, division, absolute_import, print_function

import re
import os
import sys
import socket
from datetime import datetime, timedelta

DOWNLOAD_PAGE = 'https://github.com/dougmassay/docximport-sigil-plugin/releases'
url = 'https://raw.githubusercontent.com/dougmassay/docximport-sigil-plugin/master/checkversion.xml'
delta = 0  # Used in GUI ... check as long as user has not disabled update checking


def string_to_date(datestring):
    return datetime.strptime(datestring, "%Y-%m-%d %H:%M:%S.%f")

def tuple_version(v):
    # No aplha characters in version strings allowed here!
    return tuple(map(int, (v.split("."))))


class UpdateChecker():
    '''
    self.delta              : How often to check -- in hours
    self.url                : url to github xml file
    self.lasttimechecked    : 'stringified' datetime object of last check
    self.lastonlineversion  : version string of last online version retrieved/stored
    self.w                  : bk._w from plugin.py
    '''
    def __init__(self, lasttimechecked, w, lastonlineversion=None):
        self.delta = delta
        self.url = url
        self.check4last = False
        if lastonlineversion is not None:
            self.check4last = True
        self.lasttimechecked = string_to_date(lasttimechecked)  # back to datetime object
        self.lastonlineversion = lastonlineversion
        self.w = w

    def is_connected(self):
        try:
            # connect to the host -- tells us if the host is reachable
            # 8.8.8.8 is a Google nameserver
            sock = socket.create_connection(('8.8.8.8', 53), 1)
            sock.close()
            return True
        except:
            pass
        return False

    def get_online_version(self):
        _online_version = None
        _version_pattern = re.compile(r'<current-version>([^<]*)</current-version>')

        try:
            from urllib.request import urlopen
        except ImportError:
            from urllib2 import urlopen

        # get the latest version from the plugin's github page
        if self.is_connected():
            try:
                response = urlopen(self.url, timeout=2)
                the_page = response.read()
                the_page = the_page.decode('utf-8', 'ignore')
                m = _version_pattern.search(the_page)
                if m:
                    _online_version = (m.group(1).strip())
            except:
                pass

        return _online_version

    def get_current_version(self):
        _version_pattern = re.compile(r'<version>([^<]*)</version>')
        _installed_version = None

        ppath = os.path.join(self.w.plugin_dir, self.w.plugin_name, "plugin.xml")
        with open(ppath,'rb') as f:
            data = f.read()
            data = data.decode('utf-8', 'ignore')
            m = _version_pattern.search(data)
            if m:
                _installed_version = m.group(1).strip()
        return _installed_version

    def update_info(self):
        _online_version = None
        _current_version = self.get_current_version()

        # only retrieve online resource if the allotted time has passed since last check
        if (datetime.now() - self.lasttimechecked > timedelta(hours=self.delta)):
            _online_version = self.get_online_version()
            # if online version is newer, make sure it hasn't been seen already
            if self.check4last:
                if _online_version is not None and tuple_version(_online_version) > tuple_version(_current_version) and _online_version != self.lastonlineversion:
                    return True, _online_version, str(datetime.now())
            else:
                if _online_version is not None and tuple_version(_online_version) > tuple_version(_current_version):
                    return True, _online_version, str(datetime.now())
        return False, _online_version, str(datetime.now())

def main():
    class w():
        def __init__(self):
            w.plugin_name = 'DOCXImport'
            w.plugin_dir = '/home/dmassay/.local/share/sigil-ebook/sigil/plugins'

    tmedt = str(datetime.now() - timedelta(hours=delta+1))
    version = '0.1.0'
    sim_w = w()
    chk = UpdateChecker(tmedt, version, sim_w)
    print(chk.update_info())
    print(tuple_version('0.3.2'))
    print(tuple_version('0.3.2') > tuple_version('0.3.20'))


if __name__ == "__main__":
    sys.exit(main())
