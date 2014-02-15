# -*- coding: utf-8 -*-
#*****************************************************************************
#       Copyright (C) 2006  Jorgen Stenarson. <jorgen.stenarson@bostream.nu>
#
#  Distributed under the terms of the BSD License.  The full license is in
#  the file COPYING, distributed as part of this software.
#*****************************************************************************
import clr
clr.AddReferenceByPartialName(u"System.Windows.Forms")
import System.Windows.Forms.Clipboard as cb

def GetClipboardText():
    text = ""
    if cb.ContainsText():
        text = cb.GetText()

    return text

def SetClipboardText(text):
    cb.SetText(text)    

if __name__ == u'__main__':
    txt = GetClipboardText()                            # display last text clipped
    print txt
     
     
     
     