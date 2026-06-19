# -*- coding: utf-8 -*-
# update 2026.06 Lululla
from Components.Language import language
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from os import environ as os_environ
import gettext

__version__ = "2.14"

PluginLanguageDomain = "FileCommander"
PluginLanguagePath = "Extensions/FileCommander/locale"


def localeInit():
    lang = language.getLanguage()[:2]  # getLanguage returns e.g. "fi_FI" for "language_country"
    os_environ["LANGUAGE"] = lang  # Enigma doesn't set this (or LC_ALL, LC_MESSAGES, LANG). gettext needs it!
    gettext.bindtextdomain(PluginLanguageDomain, resolveFilename(SCOPE_PLUGINS, PluginLanguagePath))


def _(txt):
    t = gettext.dgettext(PluginLanguageDomain, txt)
    if t == txt:
        # print "[FileCommander] fallback to default translation for", txt
        t = gettext.gettext(txt)
    return t


def ngettext(singular, plural, n):
    t = gettext.dngettext(PluginLanguageDomain, singular, plural, n)
    if t in (singular, plural):
        t = gettext.ngettext(singular, plural, n)
    return t


localeInit()
language.addCallback(localeInit)
