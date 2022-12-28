# for localized messages
from . import _

from Screens.Screen import Screen
from Components.ConfigList import ConfigListScreen
from Components.config import configfile, ConfigYesNo, config, getConfigListEntry
from Components.ActionMap import ActionMap
from Components.Label import Label
from enigma import eTimer, getDesktop
from Components.Sources.Source import Source
from Components.GUIComponent import GUIComponent
from .plugin import VERSION

_session = None
myskinname = None

config.plugins.ScreenNames.enable = ConfigYesNo(default=False)
cfg = config.plugins.ScreenNames
screenwidth = getDesktop(0).size()


class ScreenNamesSetupMenu(Screen, ConfigListScreen):
    if screenwidth.width() > 1280:
        skin = """
    <screen name="ScreenNames" position="center,center" size="600,315" title="" backgroundColor="#31000000" >
        <widget name="config" position="10,10" size="580,200" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
        <widget name="key_red" position="0,287" zPosition="2" size="120,30" valign="center" halign="center" font="Regular;24" transparent="1" foregroundColor="red" />
        <widget name="key_green" position="120,287" zPosition="2" size="120,30" valign="center" halign="center" font="Regular;24" transparent="1" foregroundColor="green" />
    </screen>"""
    else:
        skin = """
    <screen name="ScreenNames" position="center,center" size="500,315" title="" backgroundColor="#31000000" >
        <widget name="config" position="10,10" size="480,200" zPosition="1" transparent="0" backgroundColor="#31000000" scrollbarMode="showOnDemand" />
        <widget name="key_red" position="0,287" zPosition="2" size="120,30" valign="center" halign="center" font="Regular;16" transparent="1" foregroundColor="red" />
        <widget name="key_green" position="120,287" zPosition="2" size="120,30" valign="center" halign="center" font="Regular;16" transparent="1" foregroundColor="green" />
    </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)

        self.onChangedEntry = []
        self.list = []
        ConfigListScreen.__init__(self, self.list, session=session, on_change=self.changedEntry)
        self.setup_title = _("Setup ScreenNames")
        self["actions"] = ActionMap(["SetupActions", "ColorActions"], {
            "cancel": self.keyCancel,
            "green": self.keySave,
            "ok": self.keySave,
            "red": self.keyCancel,
        }, -2)

        self["key_green"] = Label(_("Save"))
        self["key_red"] = Label(_("Cancel"))
        self.runSetup()
        self.onLayoutFinish.append(self.layoutFinished)

    def layoutFinished(self):
        self.setTitle(_("Setup ScreenNames") + "  " + VERSION)

    def runSetup(self):
        self.list = [getConfigListEntry(_("Enable ScreenNames"), cfg.enable)]
        if cfg.enable.value:
            self.list.extend((
                getConfigListEntry(_("Display plugin in"), cfg.where),
            ))

        self["config"].list = self.list
        self["config"].setList(self.list)

    def keySave(self):
        for x in self["config"].list:
            x[1].save()
        configfile.save()
        self.close()

    def keyCancel(self):
        for x in self["config"].list:
            x[1].cancel()
        self.close()

    def changedEntry(self):
        for x in self.onChangedEntry:
            x()


class ScreenNamesAutoMain():
    def __init__(self):
        self.dialog = None

    def startScreenNames(self, session):
        self.dialog = session.instantiateDialog(ScreenNamesAutoScreen)
        self.makeShow()

    def makeShow(self):
        if cfg.enable.value:
            Screen.show = myshow
            self.dialog.show()
        else:
            self.dialog.hide()


ScreenNamesAuto = ScreenNamesAutoMain()


class ScreenNamesAutoScreen(Screen):
    if screenwidth.width() > 1280:
        skin = """<screen name="ScreenNamesAutoScreen" position="0,0" size="1920,50" title="ScreenNames Status" backgroundColor="#31ff0000" flags="wfNoBorder" zPosition="100">
        <widget name="message_label" position="0,0" size="1920,50" font="Regular;24" backgroundColor="#31ff0000" valign="center" halign="left" transparent="1" zPosition="101"/>
        </screen>"""
    else:
        skin = """<screen name="ScreenNamesAutoScreen" position="0,0" size="1280,50" title="ScreenNames Status" backgroundColor="#31ff0000" flags="wfNoBorder" zPosition="100">
        <widget name="message_label" position="0,0" size="1280,32" font="Regular;16" backgroundColor="#31ff0000" valign="center" halign="left" transparent="1" zPosition="101" />
        </screen>"""

    def __init__(self, session):
        Screen.__init__(self, session)
        global _session
        _session = session
        self.skin = ScreenNamesAutoScreen.skin
        self['message_label'] = Label()

        self.ScreenNamesTimer = eTimer()
        try:
            self.ScreenNamesTimer_conn = self.ScreenNamesTimer.timeout.connect(self.__makeWhatYouNeed)
        except:
            self.ScreenNamesTimer.callback.append(self.__makeWhatYouNeed)

        self.state = None
        self.onLayoutFinish.append(self.__chckState)

    def __chckState(self):
        if self.instance:
            self.state = cfg.enable.value
            if cfg.enable.value and ScreenNamesAuto.dialog is not None:
                ScreenNamesAuto.dialog.show()

        self.ScreenNamesTimer.start(100, True)

    def __makeWhatYouNeed(self):
        if cfg.enable.value:
            if self.instance:
                self['message_label'].setText(myskinname)
                if cfg.enable.value and ScreenNamesAuto.dialog is not None:
                    ScreenNamesAuto.dialog.show()


def myshow(self):
    try:
        ScreenNamesAuto.dialog.hide()
    except:
        pass

    print("[Screen] Showing screen '%s'." % self.skinName)  # To ease identification of screens.
    # DEBUG: if (self.shown and self.alreadyShown) or not self.instance:
    if (self.shown and self.already_shown) or not self.instance:
        return
    self.shown = True
    # DEBUG: self.alreadyShown = True
    self.already_shown = True
    self.instance.show()
    for x in self.onShow:
        x()
    for val in list(self.values()) + self.renderer:
        if isinstance(val, GUIComponent) or isinstance(val, Source):
            val.onShow()

    if cfg.enable.value:
        if self.skinName != "RdsInfoDisplay" and self.skinName != "ScreenNamesAutoScreen" and "InfoBar" not in str(self.skinName) and "Summary" not in str(self.skinName) and "_summary" not in str(self.skinName):
            global myskinname
            myskinname = str(self.skinName)
            ScreenNamesAuto.dialog = None
            ScreenNamesAuto.startScreenNames(_session)
