# for localized messages

from .plugin import cfg

from enigma import eTimer, getDesktop
from Components.Label import Label
from Components.Sources.Source import Source
from Components.GUIComponent import GUIComponent
from Screens.Screen import Screen

_session = None
myscreenname = None

screenwidth = getDesktop(0).size()


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


def myshow(self):
    # https://github.com/openatv/Enigma2/blob/master/lib/python/Screens/Screen.py
    try:
        ScreenNamesAuto.dialog.hide()
    except:
        pass

    print("[Screen] Showing screen '%s'." % self.skinName)  # To ease identification of screens.

    try:

        if (self.shown and self.already_shown) or not self.instance:
            return
        self.shown = True
        self.already_shown = True
        self.instance.show()
        for x in self.onShow:
            x()
        for val in list(self.values()) + self.renderer:
            if isinstance(val, GUIComponent) or isinstance(val, Source):
                val.onShow()
    except:
        # openatv 7.4
        if not (self.shown and self.alreadyShown) and self.instance:
            self.shown = True
            self.alreadyShown = True
            self.instance.show()
            for method in self.onShow:
                method()
            for value in list(self.values()) + self.renderer:
                if isinstance(value, GUIComponent) or isinstance(value, Source):
                    value.onShow()

    if cfg.enable.value:
        if self.skinName != "RdsInfoDisplay" and self.skinName != "ScreenNamesAutoScreen" and "InfoBar" not in str(self.skinName) and "Summary" not in str(self.skinName) and "_summary" not in str(self.skinName):
            global myscreenname
            myscreenname = str(self.skinName)
            ScreenNamesAuto.dialog = None
            ScreenNamesAuto.startScreenNames(_session)


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
                self['message_label'].setText(myscreenname)
