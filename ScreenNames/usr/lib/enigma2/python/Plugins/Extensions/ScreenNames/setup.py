
# setup.py
from enigma import getDesktop
from Components.ActionMap import ActionMap
from Components.ConfigList import ConfigListScreen
from Components.config import configfile, getConfigListEntry
from Components.Label import Label
from Screens.MessageBox import MessageBox
from Screens.Screen import Screen
from Screens import Standby

from .plugin import VERSION, cfg
from . import _

import os

screenwidth = getDesktop(0).size()
isDreambox = os.path.exists("/usr/bin/apt-get")


class ScreenNamesSetupMenu(Screen, ConfigListScreen):

    if not isDreambox:
        if screenwidth.width() > 1280:
            skin = """
        <screen name="ScreenNames" position="center,center" size="600,315" title="" backgroundColor="000000" >
            <widget name="config" position="10,10" size="580,200" zPosition="1" font="Regular;24" secondfont="Regular;24" transparent="0" backgroundColor="#000000" scrollbarMode="showOnDemand" itemHeight="36" valign="center"/>
            <widget name="key_red" position="0,287" zPosition="2" size="120,30" valign="center" halign="center" font="Regular;24" transparent="1" foregroundColor="#ff0011" />
            <widget name="key_green" position="120,287" zPosition="2" size="120,30" valign="center" halign="center" font="Regular;24" transparent="1" foregroundColor="#307e13" />
        </screen>"""
        else:
            skin = """
        <screen name="ScreenNames" position="center,center" size="500,315" title="" backgroundColor="#000000" >
            <widget name="config" position="10,10" size="480,200" zPosition="1" transparent="0" backgroundColor="#000000" font="Regular;16" secondfont="Regular;16" scrollbarMode="showOnDemand" itemHeight="24" valign="center"/>
            <widget name="key_red" position="0,287" zPosition="2" size="120,30" valign="center" halign="center" font="Regular;16" transparent="1" foregroundColor="#ff0011" />
            <widget name="key_green" position="120,287" zPosition="2" size="120,30" valign="center" halign="center" font="Regular;16" transparent="1" foregroundColor="#307e13" />
        </screen>"""
    else:
        if screenwidth.width() > 1280:
            skin = """
        <screen name="ScreenNames" position="center,center" size="600,315" title="" backgroundColor="000000" >
            <widget name="config" position="10,10" size="580,200" zPosition="1" transparent="0" backgroundColor="#000000" scrollbarMode="showOnDemand" itemHeight="36" valign="center"/>
            <widget name="key_red" position="0,287" zPosition="2" size="120,30" valign="center" halign="center" font="Regular;24" transparent="1" foregroundColor="#ff0011" />
            <widget name="key_green" position="120,287" zPosition="2" size="120,30" valign="center" halign="center" font="Regular;24" transparent="1" foregroundColor="#307e13" />
        </screen>"""
        else:
            skin = """
        <screen name="ScreenNames" position="center,center" size="500,315" title="" backgroundColor="#000000" >
            <widget name="config" position="10,10" size="480,200" zPosition="1" transparent="0" backgroundColor="#000000" scrollbarMode="showOnDemand" itemHeight="24" valign="center"/>
            <widget name="key_red" position="0,287" zPosition="2" size="120,30" valign="center" halign="center" font="Regular;16" transparent="1" foregroundColor="#ff0011" />
            <widget name="key_green" position="120,287" zPosition="2" size="120,30" valign="center" halign="center" font="Regular;16" transparent="1" foregroundColor="#307e13" />
        </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        self.session = session
        self.setup_title = _("Setup ScreenNames")
        self.onChangedEntry = []
        self.list = []
        ConfigListScreen.__init__(self, self.list, session=self.session, on_change=self.changedEntry)

        self["actions"] = ActionMap(["SetupActions", "ColorActions"], {
            "cancel": self.cancel,
            "green": self.save,
            "ok": self.save,
            "red": self.cancel,
        }, -2)

        self["key_green"] = Label(_("Save"))
        self["key_red"] = Label(_("Cancel"))
        self.initConfig()
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        self.setTitle(_("Setup ScreenNames") + "  " + VERSION)

    def initConfig(self):
        self.cfg_enable = getConfigListEntry(_("Enable ScreenNames"), cfg.enable)
        self.createSetup()

    def createSetup(self):
        self.list = []
        self.list.append(self.cfg_enable)
        self["config"].list = self.list
        self["config"].l.setList(self.list)

    def save(self):
        for x in self["config"].list:
            x[1].save()
        configfile.save()
        self.changedFinished()
        self.close()

    def cancel(self, answer=None):
        if answer is None:
            if self["config"].isChanged():
                self.session.openWithCallback(self.cancel, MessageBox, _("Really close without saving settings?"))
            else:
                self.close()
        elif answer:
            for x in self["config"].list:
                x[1].cancel()
            self.close()
        return

    def changedEntry(self):
        for x in self.onChangedEntry:
            x()

    def changedFinished(self):
        self.session.openWithCallback(self.ExecuteRestart, MessageBox, _("You need to restart the GUI") + "\n" + _("Do you want to restart now?"), MessageBox.TYPE_YESNO)
        self.close()

    def ExecuteRestart(self, result=None):
        if result:
            Standby.quitMainloop(3)
        else:
            self.close()
