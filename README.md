# FileCommander v2.14

File Manager for Enigma2

## Overview

FileCommander is a powerful two-panel file manager for Enigma2-based receivers. It supports file operations (copy, move, delete, rename), archive extraction, text viewing, image viewing, script execution, and much more.

---

## What's New in v2.14

This release introduces native image viewing, unified archive extraction, a dedicated text viewer, improved skin handling, and translation error resilience.

### New Features

- Native Image Viewer: New show_image_with_fallback() using ePicLoad - no external dependencies (no PicturePlayer required). Displays PNG, JPG, GIF, BMP directly.
- Unified Archive Extraction: New archive_utils.py module supports extracting .zip, .rar, .tar, .tgz, .gz archives to the target directory with progress feedback.
- TextViewer: Dedicated read-only text viewer for files up to 1MB. Replaces vEditor for viewing; editing is still available via menu.
- Better Unknown File Handling: Falls back to system openFile for unknown MIME types; prompts to open as text if no viewer is found.
- 1280x720 Skin: Added full HD-ready skin optimized for 720p displays.
- Translation Error Resilience: Added try/except blocks in _() and ngettext() to prevent plugin crashes when .mo files are corrupted.

### Bug Fixes

- Skin itemHeight Error: Removed itemHeight from Label widgets (list_left_head1, list_right_head1, list_left_select, list_right_select) to prevent skin parsing failures.
- None Directory Crash: Fixed AttributeError when changeDir receives None by bypassing the problematic setter in FileList.py.
- current_mountpoint Missing: Added self.current_mountpoint = None in FileList.__init__ to prevent AttributeError during base class initialization.
- gettext ValueError: Fixed "too many values to unpack (expected 2, got 20)" error caused by corrupted .mo files. Added error handling in _() and ngettext().
- PicturePlayer Dependency: Removed dependency on external PicturePlayer extension. Now uses native ePicLoad for image display.
- showiframe Callback Error: Replaced showiframe callback with native ePicLoad approach. No more "takes 0 positional arguments but 2 were given" errors.
- keyRecord Warning: Commented out unused keyRecord and showMovies actions to silence "Undefined action" warnings.
- LoadPixmap Fallback: Added fallback for LoadPixmap to prevent crashes when loading icons.

---


## File Structure

FileCommander/
├── __init__.py              (UPDATED: try/except in _() and ngettext())
├── archive_utils.py         (NEW: unified archive extraction)
├── Console.py
├── Directories.py
├── FileCommander.png
├── FileList.py              (FIXED: None handling in changeDir)
├── FileTransfer.py
├── InputBox.py
├── plugin.py
├── TaskList.py
├── TextViewer.py            (NEW: read-only text viewer)
├── ui.py                    (FIXED: skin itemHeight, 1280x720 skin)
├── UnitConversions.py
├── addons/
│   ├── __init__.py          (UPDATED: try/except in _() and ngettext())
│   ├── key_actions.py       (INTEGRATED: archive_utils, TextViewer, image viewer)
│   ├── type_utils.py        (UPDATED: show_image_with_fallback using ePicLoad)
│   ├── unrar.py
│   ├── tar.py
│   ├── unzip.py
│   ├── gz.py
│   ├── ipk.py
│   └── ...
├── images/
│   └── *.png                (File type icons)
├── pic/
│   └── button_*.png         (Color button icons)
└── locale/
    └── */LC_MESSAGES/       (Translations - fallback to English if corrupted)

---

## Installation

### From Plugin Feed
1. Press Menu -> Plugins -> Download Plugins.
2. Find FileCommander and install.

---

## Configuration

Configuration is available via:
- Menu -> Plugins -> FileCommander -> Settings
- Or by pressing MENU inside the plugin.

### Key Settings

- Filter extension: Filter files by extension (movies, music, pictures, custom).
- Count directory content: Calculate directory size in file info.
- Save cursor position: Remember last selected file across sessions.
- Default folder: Set the default directory for quick navigation.
- All movie extensions: Copy/move associated files (.eit, .meta, .cuts, etc.).
- Unknown extension as text: Attempt to open unknown files as text.
- File checksums/hashes: Choose between MD5, SHA1, SHA256, SHA512.

---

## Key Shortcuts

- OK: Open file/directory
- LEFT/RIGHT: Switch active panel
- UP/DOWN: Navigate list
- CH+ / CH-: Page up/down
- 0: Refresh screen
- 1: Toggle directory size walk
- 2: Rename file/directory
- 3: View/Edit file (< 1MB)
- 7: Create directory
- 8: Show task list
- RED: Delete file/directory
- GREEN: Move to target panel
- YELLOW: Copy to target panel
- BLUE: Rename
- INFO: File status information
- RECORD: Enter multi-selection mode

---

## Multi-Selection Mode

- OK: Toggle selection of current item
- BLUE: Invert selection
- 2: Select group (by name)
- 5: Deselect group
- 6: Toggle "move selector" option
- GREEN/YELLOW/RED: Move/Copy/Delete selected items

---

## Supported File Types

### Archives (extract)
.zip, .rar, .tar, .tgz, .gz (via archive_utils.py)
.ipk (via dedicated menu)

### Media
.ts, .mpg, .mpeg, .mkv, .avi, .mp4, .divx, .wmv, .mov, .flv, .3gp
Audio: .mp3, .ogg, .flac, .wav, .m4a, .aac
DVD: .iso, .vob, .ifo

### Images (native viewer - no external dependencies)
.jpg, .jpeg, .png, .gif, .bmp, .mvi

### Text (view only)
.txt, .log, .py, .xml, .html, .meta, .bak, .lst, .cfg, .conf, .srt

### Scripts
.sh, .py, .pyo (run or view)

---

## Changelog

### v2.14 (2024-06-19)

Added
- Native image viewer using ePicLoad - no external dependencies (PicturePlayer not required).
- archive_utils.py - unified archive extraction for .zip, .rar, .tar, .tgz, .gz.
- TextViewer.py - dedicated read-only text viewer.
- Skin support for 1280x720 resolutions.
- Fallback to system openFile for unknown MIME types.
- Prompt to open unknown files as text if no viewer is available.
- try/except blocks in _() and ngettext() to prevent crashes from corrupted .mo files.

Fixed
- Skin itemHeight errors on Label widgets (FULLHD skin).
- AttributeError: 'FileList' object has no attribute 'current_mountpoint'.
- TypeError when changeDir receives None (bypasses base setter).
- ValueError: too many values to unpack (expected 2, got 20) from corrupted translations.
- showiframe callback error (takes 0 positional arguments but 2 were given).
- Removed dependency on PicturePlayer extension for image viewing.
- LoadPixmap fallback to prevent missing icon crashes.
- keyRecord "Undefined action" warnings (commented out unused bindings).

Changed
- onFileAction now uses extract_archive for archive files (.zip, .rar, .tar, .tgz, .gz).
- onFileAction now uses TextViewer for text files instead of vEditor (view-only).
- onFileAction now uses show_image_with_fallback() for image files (native ePicLoad).
- Preserved None values for mountpoint lists instead of converting to empty strings.
- Translation system now gracefully falls back to English if .mo files are corrupted.

---

## Credits

- Original plugin ported from OpenATV to OpenPLi by mrvica (April 2019)
- Fixed and rebuilt by ims (May 2020)
- Updated by Lululla (August 2024)
- v2.14 enhancements by community contributors

---

## License

This plugin is distributed under the terms of the GNU General Public License (GPL) v2.0 or later.

---

FileCommander - Manage your files with ease.
