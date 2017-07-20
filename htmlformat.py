# -*- coding: utf-8 -*-
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

from __future__ import unicode_literals, division, absolute_import, print_function

import textwrap

import regex
import sigil_gumbo_bs4_adapter as gumbo_bs4


HTML = textwrap.dedent('''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
  "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">

<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  {0}
  <title></title>
</head>
<body>
{1}
</body>
</html>''')

LINK_TEXT = '<link href="../Styles/stylesheet.css" type="text/css" rel="stylesheet"/>'

def build_html(fragment, css=False):
    fragment = regex.sub(r'<p([^>])*></p>', r'<p\1>&#160;</p>', fragment)
    css_link = ''
    if css:
        css_link = LINK_TEXT
    new = HTML.format(css_link, fragment)
    soup = gumbo_bs4.parse(new)
    return soup.serialize_xhtml()
