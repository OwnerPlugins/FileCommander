#!/usr/bin/python
# -*- coding: utf-8 -*-
# RAED & mfaraj57 &  (c) 2018
# mod Lululla 20240720
# Improved version with save/hide/show features
# update 2026.06
from __future__ import print_function
from enigma import eConsoleAppContainer
from Screens.Screen import Screen
from Components.Label import Label
from Components.ActionMap import ActionMap
from Components.ScrollLabel import ScrollLabel
from Screens.MessageBox import MessageBox
from enigma import getDesktop
import sys
from time import time, localtime

from . import _

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3


def getDesktopSize():
    s = getDesktop(0).size()
    return (s.width(), s.height())


def isHD():
    desktopSize = getDesktopSize()
    return desktopSize[0] == 1280


class Console(Screen):
    if isHD():
        skin = '''<screen position="17,center" size="1245,681" title="Command execution..." backgroundColor="#16000000" flags="wfNoBorder">
            <widget name="text" position="9,48" size="1237,587" backgroundColor="#16000000" foregroundColor="#00ffffff" font="Console;24"/>
            <eLabel text="Command execution..." font="Regular;30" size="1000,40" position="8,3" foregroundColor="#00ffffff" backgroundColor="#16000000" zPosition="4"/>
            <eLabel position="10,674" size="165,5" backgroundColor="#00ff2525" zPosition="1"/>
            <eLabel position="238,674" size="165,5" backgroundColor="#00389416" zPosition="1"/>
            <eLabel position="1068,674" size="165,5" backgroundColor="#000080ff" zPosition="1"/>
            <eLabel text="Cancel" position="10,646" zPosition="2" size="165,30" font="Regular;24" halign="center" valign="center" backgroundColor="#16000000" foregroundColor="#00ffffff" transparent="1"/>
            <eLabel text="Hide/Show" position="238,646" zPosition="2" size="165,30" font="Regular;24" halign="center" valign="center" backgroundColor="#16000000" foregroundColor="#00ffffff" transparent="1"/>
            <eLabel text="Restart GUI" position="1068,646" zPosition="2" size="165,30" font="Regular;24" halign="center" valign="center" backgroundColor="#16000000" foregroundColor="#00ffffff" transparent="1"/>
        </screen>'''
    else:
        skin = '''<screen position="center,center" size="1886,1051" title="Command execution..." backgroundColor="#16000000" flags="wfNoBorder">
            <widget name="text" position="9,93" size="1868,897" backgroundColor="#16000000" foregroundColor="#00ffffff" font="Console;33"/>
            <eLabel text="Command execution..." font="Regular;45" size="1163,80" position="8,3" foregroundColor="#00ffffff" backgroundColor="#16000000" zPosition="4"/>
            <eLabel position="10,1043" size="250,5" backgroundColor="#00ff2525" zPosition="1"/>
            <eLabel position="353,1043" size="250,5" backgroundColor="#00389416" zPosition="1"/>
            <eLabel position="1626,1043" size="250,5" backgroundColor="#000080ff" zPosition="1"/>
            <eLabel text="Cancel" position="10,1004" zPosition="2" size="250,40" font="Regular;28" halign="center" valign="center" backgroundColor="#16000000" foregroundColor="#00ffffff" transparent="1"/>
            <eLabel text="Hide/Show" render="Label" position="353,1004" zPosition="2" size="250,40" font="Regular;28" halign="center" valign="center" backgroundColor="#16000000" foregroundColor="#00ffffff" transparent="1"/>
            <eLabel text="Restart GUI" position="1626,1004" zPosition="2" size="250,40" font="Regular;28" halign="center" valign="center" backgroundColor="#16000000" foregroundColor="#00ffffff" transparent="1"/>
        </screen>'''

    def __init__(self, session, title='Console', cmdlist=None, finishedCallback=None, closeOnSuccess=False, showStartStopText=True, skin=None):
        Screen.__init__(self, session)
        self.finishedCallback = finishedCallback
        self.closeOnSuccess = closeOnSuccess
        self.showStartStopText = showStartStopText

        if skin:
            self.skinName = [skin, 'Console']

        self.errorOcurred = False
        self.screen_hide = False
        self.cancel_msg = None
        self.output_file = ''

        self['text'] = ScrollLabel('')
        self['key_red'] = Label(_('Cancel'))
        self['key_green'] = Label(_('Hide/Show'))
        self['key_blue'] = Label(_('Restart'))
        self["actions"] = ActionMap(
            ["WizardActions", "DirectionActions", 'ColorActions'],
            {
                "ok": self.cancel,
                "back": self.cancel,
                "up": self.key_up,
                "down": self.key_down,
                "red": self.key_red,
                "green": self.key_green,
                "blue": self.restartenigma,
                "exit": self.cancel,
            }, -1
        )

        self.newtitle = title
        self.cmdlist = isinstance(cmdlist, list) and cmdlist or [cmdlist]
        self.onShown.append(self.updateTitle)

        self.container = eConsoleAppContainer()
        self.run = 0
        self.finished = False
        try:
            self.container.appClosed.append(self.runFinished)
            self.container.dataAvail.append(self.dataAvail)
        except:
            self.container.appClosed_conn = self.container.appClosed.connect(self.runFinished)
            self.container.dataAvail_conn = self.container.dataAvail.connect(self.dataAvail)

        self.onLayoutFinish.append(self.startRun)

    def updateTitle(self):
        self.setTitle(self.newtitle)

    def doExec(self, cmd):
        if isinstance(cmd, (list, tuple)):
            return self.container.execute(cmd[0], *cmd[1:])
        else:
            return self.container.execute(cmd)

    def startRun(self):
        if self.showStartStopText:
            self['text'].setText(_('Execution progress\n\n'))
        print('[Console] executing in run', self.run, ' the command:', self.cmdlist[self.run])
        if self.doExec(self.cmdlist[self.run]):
            self.runFinished(-1)

    def runFinished(self, retval):
        if retval:
            self.errorOcurred = True
            self.show()
        self.run += 1
        if self.run != len(self.cmdlist):
            if self.doExec(self.cmdlist[self.run]):
                self.runFinished(-1)
        else:
            self.finished = True
            if self.cancel_msg:
                self.cancel_msg.close()
            if self.showStartStopText:
                self['text'].appendText('\n' + _('Execution finished!!'))
            if self.finishedCallback is not None:
                self.finishedCallback()
            if not self.errorOcurred and self.closeOnSuccess:
                self.cancel()
            else:
                self['text'].appendText('\n' + _('Press OK or Exit to abort!'))
                self['key_red'].setText(_('Exit'))
                self['key_green'].setText('')

    def key_up(self):
        if self.screen_hide:
            self.toggleScreenHide()
            return
        self["text"].pageUp()

    def key_down(self):
        if self.screen_hide:
            self.toggleScreenHide()
            return
        self["text"].pageDown()

    def key_green(self):
        if self.screen_hide:
            self.toggleScreenHide()
            return
        if self.output_file == 'end':
            return
        elif self.output_file.startswith('/tmp/'):
            self["text"].setText(self.readFile(self.output_file))
            self["key_green"].setText('')
            self.output_file = 'end'
        elif self.finished:
            self.saveOutputText()
        else:
            self.toggleScreenHide()

    def key_red(self):
        if self.screen_hide:
            self.toggleScreenHide()
            return
        if self.finished:
            self.cancel()
        else:
            self.cancel_msg = self.session.openWithCallback(
                self.cancelCB,
                MessageBox,
                _('Cancel execution?'),
                type=MessageBox.TYPE_YESNO,
                default=False
            )

    def cancelCB(self, ret=None):
        self.cancel_msg = None
        if ret:
            self.cancel(True)

    def toggleScreenHide(self, setshow=False):
        if self.screen_hide or setshow:
            self.show()
        else:
            self.hide()
        self.screen_hide = not (self.screen_hide or setshow)

    def saveOutputText(self):
        lt = localtime(time())
        self.output_file = '/tmp/%02d%02d%02d_console.txt' % (lt[3], lt[4], lt[5])
        self.session.openWithCallback(
            self.saveOutputTextCB,
            MessageBox,
            _("Save the output to a file?\n('%s')") % self.output_file,
            type=MessageBox.TYPE_YESNO,
            default=True
        )

    def saveOutputTextCB(self, ret=None):
        if ret:
            try:
                text = self["text"].getText()
                with open(self.output_file, 'w') as f:
                    f.write(text)
                self["key_green"].setText(_("Load"))
            except Exception as e:
                self.output_file = 'end'
                self["key_green"].setText('')
                self.session.open(
                    MessageBox,
                    _("Error saving: %s") % str(e),
                    MessageBox.TYPE_ERROR
                )
        else:
            self.output_file = ''

    def readFile(self, filepath):
        try:
            with open(filepath, 'r') as f:
                return f.read()
        except Exception as e:
            return _("Cannot read file: %s") % str(e)

    def cancel(self, force=False):
        if self.screen_hide:
            self.toggleScreenHide()
            return
        if force or self.finished:
            self.close()
            try:
                self.container.appClosed.remove(self.runFinished)
                self.container.dataAvail.remove(self.dataAvail)
            except:
                pass
            if not self.finished:
                self.container.kill()

    def dataAvail(self, data):
        if PY3:
            text = data.decode()
        else:
            text = data
        print("[Console] Data received: ", text)
        self['text'].appendText(text)

    def restartenigma(self):
        from Screens.Standby import TryQuitMainloop
        self.session.open(TryQuitMainloop, 3)
