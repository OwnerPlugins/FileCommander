# -*- coding: utf-8 -*-
from Screens.Screen import Screen
from Components.ScrollLabel import ScrollLabel
from Components.ActionMap import ActionMap
from Components.Label import Label
from Tools.Directories import fileExists
# update 2026.06 Lululla


class TextViewer(Screen):
    """Simple text file viewer with scroll."""
    skin = """
        <screen name="TextViewer" position="center,center" size="800,600" title="Text Viewer">
            <widget name="text" position="10,10" size="780,540" font="Regular;22" />
            <widget name="key_red" position="10,560" size="100,30" font="Regular;22" halign="center" valign="center" transparent="1" />
            <widget name="key_green" position="120,560" size="100,30" font="Regular;22" halign="center" valign="center" transparent="1" />
        </screen>"""

    def __init__(self, session, filepath):
        Screen.__init__(self, session)
        self.filepath = filepath
        self["text"] = ScrollLabel("")
        self["key_red"] = Label("Close")
        self["key_green"] = Label("Close")

        self["actions"] = ActionMap(["OkCancelActions", "NavigationActions"], {
            "cancel": self.close,
            "ok": self.close,
            "up": self["text"].pageUp,
            "down": self["text"].pageDown,
            "left": self["text"].pageUp,
            "right": self["text"].pageDown,
        }, -1)

        self.onLayoutFinish.append(self.loadFile)

    def loadFile(self):
        if not fileExists(self.filepath):
            self["text"].setText("File not found.")
            return
        try:
            with open(self.filepath, "r") as f:
                content = f.read()
            self["text"].setText(content)
        except UnicodeDecodeError:
            # Try with different encoding (ISO-8859-1)
            try:
                with open(self.filepath, "r", encoding="iso-8859-1") as f:
                    content = f.read()
                self["text"].setText(content)
            except Exception as e:
                self["text"].setText("Cannot display file: %s" % str(e))
        except Exception as e:
            self["text"].setText("Error reading file: %s" % str(e))
