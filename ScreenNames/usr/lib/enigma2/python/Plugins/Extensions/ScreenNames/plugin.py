# for localized messages
from . import _

from Plugins.Plugin import PluginDescriptor
from Components.config import ConfigSubsection, config, ConfigSelection

VERSION = "1.02"

config.plugins.ScreenNames = ConfigSubsection()
config.plugins.ScreenNames.where = ConfigSelection(default="0", choices=[("0", _("plugins")), ("1", _("menu-system")), ("2", _("extensions"))])


def startSetup(menuid, **kwargs):
    if menuid != "system":
        return []
    return [(_("Setup ScreenNames"), main, "ScreenNames", None)]


def sessionAutostart(reason, **kwargs):
    if reason == 0:
        from . import ui
        ui.ScreenNamesAuto.startScreenNames(kwargs["session"])


def main(session, **kwargs):
    from . import ui
    session.open(ui.ScreenNamesSetupMenu)


def Plugins(path, **kwargs):
    name = "ScreenNames"
    descr = _("Show Skin Screen Names")
    list = [PluginDescriptor(where=[PluginDescriptor.WHERE_SESSIONSTART], fnc=sessionAutostart), ]
    if config.plugins.ScreenNames.where.value == "0":
        list.append(PluginDescriptor(name=name, description=descr, where=PluginDescriptor.WHERE_PLUGINMENU, needsRestart=True, fnc=main))
    elif config.plugins.ScreenNames.where.value == "1":
        list.append(PluginDescriptor(name=name, description=descr, where=PluginDescriptor.WHERE_MENU, needsRestart=True, fnc=startSetup))
    elif config.plugins.ScreenNames.where.value == "2":
        list.append(PluginDescriptor(name=name, description=descr, where=PluginDescriptor.WHERE_EXTENSIONSMENU, needsRestart=True, fnc=main))
    return list
