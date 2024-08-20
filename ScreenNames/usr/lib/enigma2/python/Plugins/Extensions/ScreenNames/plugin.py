# for localized messages
from . import _
from Plugins.Plugin import PluginDescriptor
from Components.config import ConfigSubsection, config, ConfigYesNo

VERSION = "1.05"

config.plugins.ScreenNames = ConfigSubsection()
cfg = config.plugins.ScreenNames
cfg.enable = ConfigYesNo(default=False)


def sessionAutostart(reason, **kwargs):
    if reason == 0:
        from . import ui
        ui.ScreenNamesAuto.startScreenNames(kwargs["session"])


def main(session, **kwargs):
    from .setup import ScreenNamesSetupMenu
    session.open(ScreenNamesSetupMenu)


def Plugins(path, **kwargs):
    name = "ScreenNames"
    descr = _("Show Skin Screen Names")
    list = [PluginDescriptor(where=[PluginDescriptor.WHERE_SESSIONSTART], fnc=sessionAutostart), ]
    list.append(PluginDescriptor(name=name, description=descr, where=PluginDescriptor.WHERE_PLUGINMENU, needsRestart=True, fnc=main))

    return list
