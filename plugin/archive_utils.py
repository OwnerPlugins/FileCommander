# -*- coding: utf-8 -*-
# new file: 2026.06 Lululla

import os
from Screens.MessageBox import MessageBox

from .Console import Console
from . import _


def extract_archive(filepath, target_dir, session):
    """
    Extract archive using system commands (unzip, tar, unrar, gunzip).
    Returns True on success, False on failure.
    """
    if not os.path.isfile(filepath):
        return False

    ext = os.path.splitext(filepath)[1].lower()
    cmd_map = {
        '.zip': ['unzip', '-o', filepath, '-d', target_dir],
        '.rar': ['unrar', 'x', '-o+', filepath, target_dir],
        '.tar': ['tar', '-xf', filepath, '-C', target_dir],
        '.tgz': ['tar', '-xzf', filepath, '-C', target_dir],
        '.gz': ['gunzip', '-c', filepath, '>', os.path.join(target_dir, os.path.basename(filepath)[:-3])],
        '.ipk': ['tar', '-xzf', filepath, '-C', target_dir],  # ipk is ar archive, but we can fallback
    }

    cmd = cmd_map.get(ext)
    if not cmd:
        session.open(MessageBox, _("Unsupported archive type."), MessageBox.TYPE_ERROR)
        return False

    # Ensure target directory exists
    if not os.path.exists(target_dir):
        try:
            os.makedirs(target_dir)
        except:
            session.open(MessageBox, _("Cannot create target directory."), MessageBox.TYPE_ERROR)
            return False

    # Run command in Console (shows progress)
    session.open(Console, title=_("Extracting..."), cmdlist=[cmd])
    return True
