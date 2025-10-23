# organize.py
# Automated File Organizer CLI Tool

import argparse #for command-line arguments
from pathlib import Path #to work with file paths
import shutil #for file operations
import sys #for error handling
import os 

# --- 1. CONFIGURATION  ---

def get_category_map() -> dict:
    """
    Defines the master mapping of file extensions to destination folder names.
    All keys must be lowercase.
    
    Returns a dictionary containing the following file extensions and their corresponding destination folder names:
        - Documents: pdf, doc, docx, txt, odt, rtf, epub, csv, xls, xlsx
        - Images: jpg, jpeg, png, gif, bmp, tiff, ico, svg
        - Videos: mp4, mov, avi, mkv, wmv
        - Audio: mp3, wav, flac, aac
        - Archives: zip, rar, 7z, tar, gz
        - Programs/Executables: exe, dmg, pkg, msi, iso
    """
    return {
        # Documents
        '.pdf': 'Documents',
        '.doc': 'Documents',
        '.docx': 'Documents',
        '.txt': 'Documents',
        '.odt': 'Documents',
        '.rtf': 'Documents',
        '.epub': 'Documents',
        '.csv': 'Documents',
        '.xls': 'Documents',
        '.xlsx': 'Documents',

        # Images
        '.jpg': 'Images',
        '.jpeg': 'Images',
        '.png': 'Images',
        '.gif': 'Images',
        '.bmp': 'Images',
        '.tiff': 'Images',
        '.ico': 'Images',
        '.svg': 'Images',

        # Videos
        '.mp4': 'Videos',
        '.mov': 'Videos',
        '.avi': 'Videos',
        '.mkv': 'Videos',
        '.wmv': 'Videos',

        # Audio
        '.mp3': 'Audio',
        '.wav': 'Audio',
        '.flac': 'Audio',
        '.aac': 'Audio',

        # Archives
        '.zip': 'Archives',
        '.rar': 'Archives',
        '.7z': 'Archives',
        '.tar': 'Archives',
        '.gz': 'Archives',

        # Programs/Executables
        '.exe': 'Applications',
        '.dmg': 'Applications',
        '.pkg': 'Applications',
        '.msi': 'Applications',
        '.iso': 'Applications',
    }
